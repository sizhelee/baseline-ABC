from NectarSource import Nectar
from Graph import Graph
from utils import io_util, utils
import numpy as np

class ABC:
    def __init__(self, config):
        self.graph = Graph(io_util.load_mtx(config["graph"]["graph_path"]))
        self.num_thread = config["global"]["num_threads"]

def main():
    config = io_util.load_yaml("./config.yml", True)
    
    

if __name__ == "__main__":
    main()