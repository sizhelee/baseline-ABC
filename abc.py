from http.client import NOT_MODIFIED
from NectarSource import Nectar
from Graph import Graph
from utils import io_util, utils
import numpy as np
import copy
from tqdm import trange

class ABC:
    def __init__(self, config):
        self.num_thread = config["global"]["num_threads"]
        self.num_bees = config["nectar"]["num_nectars"]
        self.num_loops = config["global"]["num_loop"]
        self.limit = config["nectar"]["limit"]

        self.graph = Graph(io_util.load_mtx(config["graph"]["graph_path"]))

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
        

    def solve(self):
        for i in trange(self.num_loops):
            self.send_employedBees()
            self.send_onlookerBees()
            self.send_scoutBees()
        return self.bestMethod


def main():

    config = io_util.load_yaml("./config.yml", True)
    model = ABC(config)
    bestMethod = model.solve()
    
    print(bestMethod.route, bestMethod.cal_trueFit())
    

if __name__ == "__main__":
    main()