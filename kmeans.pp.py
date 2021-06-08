import numpy as np
import pandas as pn
import mykmeanssp as km
import sys

# Reading the arguments from command line:
arglen= len(sys.argv)
assert (arglen==2 or arglen==3) # making sure we have just 2 arguments (K and MAX_ITER) or just 1 (K)
K= int(sys.argv[1])
assert (K>0)
if (arglen==2):
    MAX_ITER=200
else:
    MAX_ITER= int(sys.argv[2])
    assert (MAX_ITER>0)

# reading the data from the file and putting n vectors in an array
data = []
while True:
    try:
        vec = []
        for num in input().split(','):
            vec.append(float(num))
        data.append(vec)
    except EOFError:
        break

N = len(data)
assert (N>K)

d = len(data[0])
assert (d>0)

# צריך לשנות את וקטור אריי להיות הדאטא שהשגנו משני הקבצים, כלומר רשימת הוקטורים הכללית.
#בנוסף צריך להחליט על מוסכמה לגבי N, האם נשנה את N להיות שווה ל2N כמו גודל הרשימות? או שצריך בקוד לשנות בכל מקום שרשום N לשנות ל2N...
Vector_array = [[1,2,3],[2,3,4]]


# implementing the algorithm using numpy as requested

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
        Cntr[z] = np.random.choice(Vector_array,p=Probabilities)
        z+=1


# this function calculates the difference between two vectors of length d
def diff(vec1, vec2):
    dif = 0
    for i in range(d):
        dif += ((vec1[i]) - (vec2[i])) ** 2
    assert isinstance(d, int)
    return dif ** (1 / 2)
        


Cntr = kmeansPP()
final_cntr = km.fit(K, N , d, MAX_ITER, Vector_array, Cntr)
