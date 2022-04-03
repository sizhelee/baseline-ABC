import numpy as np

def build_graph_from_edge(list_edge):
    num_nodes = np.max(list_edge) + 1
    graph = [[] for i in range(num_nodes)]
    for edge in list_edge:
        graph[edge[0]].append(edge[1])
    return graph

def cal_indegree_from_edge(list_edge):
    num_nodes = np.max(list_edge) + 1
    in_degree = [0 for i in range(num_nodes)]
    for edge in list_edge:
        in_degree[edge[1]] += 1
    return in_degree