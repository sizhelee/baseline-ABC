import random
import os

def rand_int(start, end):
    return random.randint(start, end)

def rand_float(start, end):
    return start + (end-start)*random.random()

def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def generate_rate(n):
    prob = [i+1 for i in range(n)]
    for i in range(int(n/3)):
        prob[n-1-i] = n-prob[n-1-i]  # 定义相对概率分布
    sum = 0
    for s in prob:
        sum += s
    for i in range(n):  # 归一化
        prob[i] /= sum
    return prob