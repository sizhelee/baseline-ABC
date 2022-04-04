import numpy as np
from numpy import dtype, random
from utils import utils
import copy


class Graph:
    def __init__(self, list_edge):
        self.list_edge = list_edge
        self.num_nodes = np.max(list_edge) + 1
        self.graph = self.build_graph_from_edge(list_edge)
        self.in_degree = self.cal_indegree_from_edge(list_edge)

    def build_graph_from_edge(self, list_edge):
        graph = [[] for i in range(self.num_nodes)]
        for edge in list_edge:
            graph[edge[0]].append(edge[1])
        return graph

    def cal_indegree_from_edge(self, list_edge):
        in_degree = [0 for i in range(self.num_nodes)]
        for edge in list_edge:
            in_degree[edge[1]] += 1
        return in_degree

    def generate_init_method(self): # generate legal random route
        route = []
        flag = np.zeros(self.num_nodes)
        in_degree = np.array(copy.deepcopy(self.in_degree))
        
        for i in range(self.num_nodes):
            mask = (flag==0)*(in_degree==0)
            idx = np.argwhere(mask).reshape(-1)
            x = random.choice(idx)
            route.append(x)
            flag[x] = 1
            for edge in self.graph[x]:
                in_degree[edge] -= 1
        return route
    
    def generate_new_method(self, route):
        rate = utils.generate_rate(self.num_nodes)
        index = np.arange(self.num_nodes, dtype="int32")
        idx = np.random.choice(index, p=rate)

        new_route = []
        flag = np.zeros(self.num_nodes)
        in_degree = np.array(copy.deepcopy(self.in_degree))

        for i in range(idx):
            new_route.append(route[i])
            flag[route[i]] = 1
            for edge in self.graph[route[i]]:
                in_degree[edge] -= 1

        for i in range(idx, self.num_nodes):
            mask = (flag==0)*(in_degree==0)
            idx = np.argwhere(mask).reshape(-1)
            x = random.choice(idx)
            new_route.append(x)
            flag[x] = 1
            for edge in self.graph[x]:
                in_degree[edge] -= 1
        
        return new_route
                
    def is_method_legal(self, method):

        route = method.route()
        flag = np.zeros(self.num_nodes)

        for node in route:
            flag[node] = 1
            if flag[self.graph[node]].any():
                return False
        return True