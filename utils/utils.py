import random

def rand_int(start, end):
    return random.randint(start, end)

def rand_float(start, end):
    return start + (end-start)*random.random()