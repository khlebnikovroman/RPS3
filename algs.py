import numpy as np
from tabulate import tabulate

inf = np.Inf


def Dijkstra(size, start, finish, matrix):
    valid = [True] * size
    weight = [inf] * size
    weight[start] = 0
    for i in range(size):
        min_weight = np.Inf
        ID_min_weight = -1
        for j in range(size):
            if valid[j] and weight[j] < min_weight:
                min_weight = weight[j]
                ID_min_weight = j
        for z in range(size):
            if weight[ID_min_weight] + matrix[ID_min_weight][z] < weight[z]:
                weight[z] = weight[ID_min_weight] + matrix[ID_min_weight][z]
        valid[ID_min_weight] = False
    return weight[finish]


def Floyd(start, finish, W):
    INF = inf
    N = len(W)
    F = [[INF] * N for i in range(N)]
    F[0][start] = 0
    for k in range(1, N):
        for i in range(N):
            F[k][i] = F[k - 1][i]
            for j in range(N):
                if F[k - 1][j] + W[j][i] < F[k][i]:
                    F[k][i] = F[k - 1][j] + W[j][i]
    print(tabulate(F))
    return F[-1][finish]

