import numpy as np

def find_dist(p1: tuple, p2: tuple):
    sum = 0
    if len(p1) != len(p2):
        return None
    else:
        for (a, b) in zip(p1, p2):
            sum += (b - a)**2
    return np.sqrt(sum)

d = find_dist((0, 0, 0), (1, 1))
print(d)