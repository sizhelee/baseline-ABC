import os
import yaml
from scipy.io import mmread
from scipy.sparse import triu
import numpy as np
import logging, logging.handlers
import json


def read_all_mtx(folder_path):
    files= os.listdir(folder_path) #得到文件夹下的所有文件名称
    all_files = []
    for file in files: #遍历文件夹
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
            all_files.append(folder_path+"/"+file)
    return all_files


def init_logger(log_path,logging_name):
    logger = logging.getLogger(logging_name)
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


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

def save_npy(file_path, data, verbose=True):
    np.save(file_path, data)
    print(data.shape)
    if verbose:
        print("Write route data to {}".format(file_path))
