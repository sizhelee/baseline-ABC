import yaml
from scipy.io import mmread
from scipy.sparse import triu
import numpy as np

def load_yaml(file_path, verbose=True):
    with open(file_path, "r") as f:
        yml_file = yaml.load(f, Loader=yaml.SafeLoader)
    if verbose:
        print("Load yaml file from {}".format(file_path))
    return yml_file

def load_mtx(file_path, verbose=True):
    edge = triu(mmread(source=file_path), k=1)
    Lis_edge = np.array([edge.row, edge.col]).transpose()
    if verbose:
        print("Load mtx data from {}".format(file_path))
    return Lis_edge