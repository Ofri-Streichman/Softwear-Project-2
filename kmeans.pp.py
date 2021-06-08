import numpy
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
else:
    MAX_ITER = int(sys.argv[2])
    assert (MAX_ITER > 0)

file1 = sys.argv[3]
file2 = sys.argv[4]

data_fromfile1 = pd.read_csv(file1, header=None)
data_fromfile2 = pd.read_csv(file2, header=None)
data = pd.merge(data_fromfile1, data_fromfile2, on=0)
vectors = data.to_numpy()
vectors = numpy.round(vectors, 4)

print(vectors)

N = len(vectors)
print(N)
assert (N > K)

d = len(vectors[0]) - 1
print(d)

print(vectors[0][0])

assert (d > 0)


Vector_array = [[1, 2, 3], [2, 3, 4]]


np.random.seed(0)
def kmeansPP ():
    z =1
    D_arr = np.shape(N)
    Cntr = np.shape(N,d)
    Cntr[0] = np.random.rand(Vector_array)
    while (z<K):
        for i in range(N):
            point = Vector_array[i]
            D_arr[i] = float('inf')
            for j in range(z):
                dif =  diff(point,Cntr[j])**2
                if diff < D_arr[i]:
                    D_arr[i]=diff
        Probsum = sum(D_arr)
        Probabilities = [(D_arr[i]/Probsum) for i in range(K)]
        Cntr[z] = np.random.choice(Vector_array, p=Probabilities)
        z+=1


# this function calculates the difference between two vectors of length d
def diff(vec1, vec2):
    dif = 0
    for i in range(d):
        dif += ((vec1[i]) - (vec2[i])) ** 2
    assert isinstance(d, int)
    return dif ** (1 / 2)


Cntr = kmeansPP()
final_cntr = km.fit(K, N, d, MAX_ITER, Vector_array, Cntr)
