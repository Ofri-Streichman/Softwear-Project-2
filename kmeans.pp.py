import copy
import numpy as np
import pandas as pd
import mykmeanssp as km
import sys

# Reading the arguments from command line:
arglen = len(sys.argv)
assert (arglen == 4 or arglen == 5)  # making sure we have just 4 args (K,MAX_ITER, 2 input files) or 3 (no MAX_ITER)
K = int(sys.argv[1])
assert (K > 0)
if arglen == 4:
    MAX_ITER = 300
    file1 = sys.argv[2]
    file2 = sys.argv[3]
else:
    MAX_ITER = int(sys.argv[2])
    file1 = sys.argv[3]
    file2 = sys.argv[4]
    assert (MAX_ITER > 0)

data_fromfile1 = pd.read_csv(file1, header=None)
data_fromfile2 = pd.read_csv(file2, header=None)
data = pd.merge(data_fromfile1, data_fromfile2, on=0)
vectors = data.to_numpy()
vectors = vectors[vectors[:, 0].argsort()]

N = len(vectors)
assert (N > K)

d = len(vectors[0]) - 1
assert (d > 0)

np.random.seed(0)

def kmeansPP():
    D_arr = np.zeros(N, dtype=float)
    Cntr = np.zeros((K, d + 1), dtype=float)
    z = np.random.choice(N)
    Cntr[0] = vectors[z]
    z = 1
    while (z < K):
        for i in range(N):
            point = vectors[i]
            D_arr[i] = float('inf')
            for j in range(z):
                dif = diff(point, Cntr[j]) ** 2
                if dif < D_arr[i]:
                    D_arr[i] = dif
        Probsum = sum(D_arr)
        Probabilities = np.array([(D_arr[i] / Probsum) for i in range(N)])
        cntr_i = np.random.choice(N, p=Probabilities)
        Cntr[z] = copy.deepcopy(vectors[cntr_i])
        z += 1
    for i in range(K - 1):
        print(int(Cntr[i][0]), end=",")
    print(int(Cntr[K - 1][0]))
    return_array = np.delete(Cntr, 0, 1).tolist()
    return return_array


# this function calculates the difference between two vectors of length d
def diff(vec1, vec2):
    dif = 0
    for i in np.arange(start=1, stop=d + 1):
        dif += ((vec1[i]) - (vec2[i])) ** 2
    return dif ** (1 / 2)


def print_cen():
    for i in range(K):
        for j in range(d - 1):
            print("{:.4f}".format(final_centroids[i][j]), end=",")
        if i < K - 1:
            print("{:.4f}".format(final_centroids[i][d - 1]))
        else:
            print("{:.4f}".format(final_centroids[i][d - 1]), end="")


# preparing the arguments for the C program
centroids_for_c = kmeansPP()
Vector_array = np.delete(vectors, 0, 1).tolist()

final_centroids = km.fit(K, N, d, MAX_ITER, Vector_array, centroids_for_c)
final_centroids = np.round(final_centroids, 4)
print_cen()
