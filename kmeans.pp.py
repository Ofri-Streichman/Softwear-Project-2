import copy
import numpy as np
import pandas as pd
import mykmeanssp as km
import sys


# Reading the arguments from command line:
arglen = len(sys.argv)
assert (arglen == 4 or arglen == 5)  # making sure we have just 5 args (K,MAX_ITER, 2 input files) or 4 (no MAX_ITER)
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

#merging the input files
data_fromfile1 = pd.read_csv(file1, header=None)
data_fromfile2 = pd.read_csv(file2, header=None)
data = pd.merge(data_fromfile1, data_fromfile2, on=0)
vectors = data.to_numpy()                               #putting the N vectors in a numpy array
vectors = vectors[vectors[:, 0].argsort()]

#making sure N>K and d>0 !
N = len(vectors)
assert (N > K)
d = len(vectors[0]) - 1
assert (d > 0)

# random seed for results
np.random.seed(0)

# implementing the Kmeans++ algorithm using numpy as described in the assignment
def kmeansPP():
    D_arr = np.zeros(N, dtype=float)
    Cntr = np.zeros((K, d + 1), dtype=float)
    cntr_i = np.random.choice(N)
    Cntr[0] = vectors[cntr_i]
    D_arr = np.full((N),np.inf)
    D_arr[cntr_i] = 0
    z = 1
    while (z < K):
        for i in range(N):
            point = vectors[i]
            dif = diff(point, Cntr[z-1]) ** 2        #in this part we only need to compare to the previous centroid
            if dif < D_arr[i]:
                D_arr[i] = dif
        Probsum = sum(D_arr)
        Probabilities = np.array([(D_arr[i] / Probsum) for i in range(N)])
        cntr_i = np.random.choice(N, p=Probabilities)
        D_arr[cntr_i]=0
        Cntr[z] = copy.deepcopy(vectors[cntr_i])
        z += 1
    # printing the centroids indices and preparing them for the C program (removing the indices)
    for i in range(K - 1):
        print(int(Cntr[i][0]), end=",")
    print(int(Cntr[K - 1][0]))
    return_array = np.delete(Cntr, 0, 1).tolist()
    return return_array


# this function calculates the difference between two vectors of length d+1 ignoring the first field which is the index
def diff(vec1, vec2):
    dif = 0
    for i in np.arange(start=1, stop=d + 1):
        dif += ((vec1[i]) - (vec2[i])) ** 2
    return dif ** (1 / 2)

#this function prints the centroids as requested in the assignment
def print_cen():
    for i in range(K):
        for j in range(d - 1):
            print(final_centroids[i][j], end=",")
        if i < K - 1:
            print(format(final_centroids[i][d - 1]))
        else:
            print(format(final_centroids[i][d - 1]), end="")


# preparing the arguments for the C program
centroids_for_c = kmeansPP()
Vector_array = np.delete(vectors, 0, 1).tolist()

final_centroids = km.fit(K, N, d, MAX_ITER, Vector_array, centroids_for_c)
final_centroids = np.round(final_centroids, 4)
print_cen()
