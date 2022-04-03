class Nectar:
    def __init__(self, graph, trail):
        self.graph = graph
        self.route = graph.generate_init_method()
        self.trail = trail
        self.trueFit = self.cal_trueFit()
        self.fitness = self.cal_fitness()

    def cal_trueFit(self):  #calculate ture time of a method
        pass

    def cal_fitness(self):  #calculate fitted value of ture fit
        pass