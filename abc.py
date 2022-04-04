from http.client import NOT_MODIFIED
from NectarSource import Nectar
from Graph import Graph
from utils import io_util, utils
import numpy as np
import copy
from tqdm import trange
import time

class ABC:
    def __init__(self, config, adjust=False):

        self.graph = Graph(io_util.load_mtx(config["graph"]["graph_path"]))

        if adjust == True:
            self.num_thread = int(self.graph.num_nodes**(1/3))+1
            self.num_bees = int(self.graph.num_nodes/8)+1
            if self.graph.num_nodes < 200:
                self.num_bees = 25
            self.num_loops = self.graph.num_nodes // 2
            if self.graph.num_nodes < 200:
                self.num_loops = 100

        else:
            self.num_thread = config["global"]["num_threads"]
            self.num_bees = config["nectar"]["num_nectars"]
            self.num_loops = config["global"]["num_loop"]
        
        self.limit = config["nectar"]["limit"]

        self.truefit = [0 for i in range(self.num_bees)]
        self.rfit = [0 for i in range(self.num_bees)]

        self.methodGroup = []
        self.employedBees = []
        self.onlookerBees = []
        for i in range(self.num_bees):
            method = Nectar(self.graph, 0, self.num_thread)
            self.methodGroup.append(copy.deepcopy(method))
            self.employedBees.append(copy.deepcopy(method))
            self.onlookerBees.append(copy.deepcopy(method))

        self.bestMethod = Nectar(self.graph, 0, self.num_thread)

    def cal_fitness(self):  #calculate fitted value of ture fit
        minfit = 1e9
        for i, method in enumerate(self.methodGroup):
            self.truefit[i] = method.cal_trueFit()
            minfit = min(minfit, self.truefit[i])
        for i, tfit in enumerate(self.truefit):
            self.rfit[i] = 0.1 + 0.9*(minfit/tfit)
            if tfit == minfit:
                self.bestMethod = copy.deepcopy(self.methodGroup[i])
        
    def send_employedBees(self):
        for i, (bee, nectar) in enumerate(zip(self.employedBees, self.methodGroup)):
            new_route = self.graph.generate_new_method(nectar.route)
            bee = Nectar(graph=self.graph, trail=0, num_threads=self.num_thread, route=new_route)
            self.employedBees[i] = copy.deepcopy(bee)

            fit = nectar.cal_trueFit()
            new_fit = bee.cal_trueFit()

            if fit > new_fit:
                self.methodGroup[i] = copy.deepcopy(bee)
                self.methodGroup[i].trail = 0
            else:
                self.methodGroup[i].trail += 1
        self.cal_fitness()

    def send_onlookerBees(self):
        i = 0
        t = 0

        while t < self.num_bees:
            r_choose = utils.rand_float(0, 1)
            if r_choose < self.rfit[i]:
                new_route = self.graph.generate_new_method(self.methodGroup[i].route)
                bee = Nectar(self.graph, 0, self.num_thread, new_route)
                self.onlookerBees[t] = copy.deepcopy(bee)

                fit = self.methodGroup[i].cal_trueFit()
                new_fit = bee.cal_trueFit()

                if fit > new_fit:
                    self.methodGroup[i] = copy.deepcopy(bee)
                    self.methodGroup[i].trail = 0
                else:
                    self.methodGroup[i].trail += 1

                t += 1

            i = (i + 1) % self.num_bees
        self.cal_fitness()

    def send_scoutBees(self):
        for i, method in enumerate(self.methodGroup):
            if method.trail >= self.limit:
                self.methodGroup[i] = Nectar(self.graph, 0, self.num_thread)
        self.cal_fitness()   

    def solve(self, save_loop=False, loop_path=None):
        routes = []
        for i in trange(self.num_loops):
            self.send_employedBees()
            self.send_onlookerBees()
            self.send_scoutBees()

            route_loop = []
            for method in self.methodGroup:
                route_loop.append(method.route)
            routes.append(route_loop)

        if save_loop:
            routes = np.array(routes)
            io_util.save_npy(loop_path, routes, False)
        return self.bestMethod

    def solve_best(self):
        dp = [1 for i in range(len(self.graph.graph))]
        for i in range(len(self.graph.graph)-1, -1, -1):
            for j in self.graph.graph[i]:
                dp[i] = max(dp[j]+1, dp[i])
        return max(dp)

    def solve_greedy(self):
        graph = self.graph.graph
        left_nodes = len(graph)
        route = 0
        flag = [0 for i in range(len(graph))]
        in_degree = copy.deepcopy(self.graph.in_degree)

        while left_nodes > 0:
            candidates = []
            for i in range(len(in_degree)):
                if in_degree[i] == 0 and flag[i] == 0:
                    candidates.append((i, len(graph[i])))

            if self.num_thread < len(candidates):
                select = sorted(candidates, key=lambda x: x[1])[-1*self.num_thread:]
                choose = [x for x, _ in select]
            else:
                choose = [x for x, _ in candidates]

            for node in choose:
                flag[node] = 1
                for end in graph[node]:
                    in_degree[end] -= 1

            left_nodes -= len(choose)
            route += 1

        return route


def main():

    config = io_util.load_yaml("./config.yml", True)
    logger = io_util.init_logger(log_path=config["global"]["log_path"], logging_name='')

    folder_mode = config["global"]["folder_mode"]
    if folder_mode:
        file_list = io_util.read_all_mtx(config["global"]["folder_path"])
    else:
        file_list = [config["graph"]["graph_path"]]

    for i, f in enumerate(file_list):

        print("running", str(i+1), "of", len(file_list))
        config["graph"]["graph_path"] = f

        model = ABC(config, adjust=config["global"]["need_adjust"])

        save_loop = config["global"]["save_loop"]

        result_abc = None
        if config["solver"]["use_abc"]:
            loop_dir = config["global"]["loop_folder"]
            utils.make_dir(loop_dir)
            loop_path = loop_dir+"/{}.npy".format(f[f.rfind('/')+1:f.rfind('.mtx')])
            
            bestMethod = model.solve(save_loop, loop_path)
            result_abc = bestMethod.cal_trueFit()
            #print(bestMethod.route, result_abc)

        result_dp = model.solve_best()

        start_time = time.time()
        result_greedy = model.solve_greedy()
        duration = time.time()-start_time

        logger.info("mtx_name: {mtx}, num_nodes: {num_nodes}, num_threads: {num_threads}, num_loop: {num_loop}, num_nectars:{num_nectars}, limit: {limit}, dp_result: {dp}, greedy_result:{greedy}, abc_result: {abc}, greedy_time:{t}".format(
                mtx=f.replace(config['global']['folder_path']+'/', ''), num_nodes=model.graph.num_nodes, 
                num_threads=model.num_thread, num_loop=model.num_loops, num_nectars=model.num_bees, 
                limit=model.limit, dp=result_dp, greedy=result_greedy,abc=result_abc, t=duration))
    

if __name__ == "__main__":
    main()