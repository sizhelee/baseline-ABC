import copy

class Nectar:
    def __init__(self, graph, trail, num_threads, route=None):
        self.graph = graph
        if route is None:
            self.route = graph.generate_init_method()
        else:
            self.route = route
        self.trail = trail
        self.num_threads = num_threads
        

    def cal_trueFit(self):  #calculate ture time of a method
        cnt = 0
        route = copy.deepcopy(self.route)
        in_degree = copy.deepcopy(self.graph.in_degree)

        while True:
            num_works = 0
            this_time = []
            for node in route:
                if in_degree[node] == 0:
                    this_time.append(node)

                    num_works += 1
                    if num_works == self.num_threads:
                        break

            for node in this_time:
                route.remove(node)
                for edge in self.graph.graph[node]:
                        in_degree[edge] -= 1
            cnt += 1
            if len(route) == 0:
                break

        return cnt