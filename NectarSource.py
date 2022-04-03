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
        route = self.route
        in_degree = self.graph.in_degree

        while True:
            num_works = 0
            this_time = []
            for i in range(len(route)):
                node = route[i]
                if in_degree[node] == 0:

                    route.remove(node)
                    i -= 1
                    this_time.append(node)

                    num_works += 1
                    if num_works == self.num_threads:
                        break

            for node in this_time:
                for edge in self.graph[node]:
                        in_degree[edge] -= 1
            cnt += 1
            if len(route) == 0:
                break

        return cnt