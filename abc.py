from http.client import NOT_MODIFIED
from NectarSource import Nectar
from Graph import Graph
from utils import io_util, utils
import numpy as np
import copy

class ABC:
    def __init__(self, config):
        self.graph = Graph(io_util.load_mtx(config["graph"]["graph_path"]))
        self.num_thread = config["global"]["num_threads"]
        self.num_bees = config["nectar"]["num_nectars"]
        self.num_loops = config["global"]["num_loop"]

        self.methodGroup = []
        self.employedBees = []
        self.OnlookerBees = []
        for i in range(self.num_bees):
            method = Nectar(self.graph.generate_init_method, 0)
            self.methodGroup.append(copy.deepcopy(method))
            self.employedBees.append(copy.deepcopy(method))
            self.OnlookerBees.append(copy.deepcopy(method))

        self.bestMethod = Nectar(self.graph.generate_init_method, 0)

    def send_employedBees(self):
        raise NotImplementedError

    
    def calculate_Probabilities(self):
        raise NotImplementedError

    def send_onlookerBees(self):
        raise NotImplementedError
    
    def send_scoutBees(self):
        raise NotImplementedError
    
    def update_best(self):
        raise NotImplementedError

    def solve(self):
        for i in range(self.num_loops):
            self.send_employedBees()
            self.calculate_Probabilities()
            self.send_onlookerBees()
            self.update_best()
            self.send_scoutBees()
            self.update_best()
        return self.bestMethod


def main():

    config = io_util.load_yaml("./config.yml", True)
    model = ABC(config)
    bestMethod = model.solve()
    
    print(bestMethod.cal_trueFit())
    

if __name__ == "__main__":
    main()