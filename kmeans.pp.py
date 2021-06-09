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
else:
    MAX_ITER = int(sys.argv[2])
    assert (MAX_ITER > 0)

file1 = sys.argv[3]
file2 = sys.argv[4]

data_fromfile1 = pd.read_csv(file1, header=None)
data_fromfile2 = pd.read_csv(file2, header=None)
data = pd.merge(data_fromfile1, data_fromfile2, on=0)
vectors = data.to_numpy()
vectors = np.round(vectors, 4)

#print(vectors)

N = len(vectors)
#print(N)
assert (N > K)

d = len(vectors[0]) - 1
#print(d)
assert (d > 0)


np.random.seed(0)
def kmeansPP ():
    D_arr = np.zeros(N,dtype=float)
    Cntr = np.zeros((N,d+1), dtype=float)
    z= np.random.choice(N)
    Cntr[0] = vectors[z]
    z=1
    while (z<K):
        for i in range(N):
            point = vectors[i]
            D_arr[i] = float('inf')
            for j in range(z):
                dif =  diff(point,Cntr[j])**2
                if dif < D_arr[i]:
                    D_arr[i]=dif
        Probsum = sum(D_arr)
        Probabilities = np.array([(D_arr[i]/Probsum) for i in range(N)])
        cntr_i = np.random.choice(N, p=Probabilities)
        Cntr[z] = copy.deepcopy(vectors[cntr_i])
        z+=1
    return_array = [Cntr[:i] for i in range(K)]
    print("the k centroids are: ")
    arr=[]
    for i in range(K):
        print(Cntr[i][0])
    return return_array

# this function calculates the difference between two vectors of length d
def diff(vec1, vec2):
    dif = 0
    for i in np.arange(start=1, stop=d+1):
        dif += ((vec1[i]) - (vec2[i])) ** 2
    return dif ** (1 / 2)


#preparing the arguments for the C program
centroids_for_c = kmeansPP()
Vector_array = []
for i in range(N):
    Vector_array.append(vectors[i][1:]) # meaning we omit the index field for every datapoint
final_cntr = km.fit(K, N, d, MAX_ITER, Vector_array, centroids_for_c)
print(final_cntr)
