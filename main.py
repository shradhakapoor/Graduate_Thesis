''' Optimal or near optimal solutions to the serial batching problem under weighted average completion '''
# author : Shradha Kapoor
# date : September 6, 2018
# python_version : 3.6


# s -- selection time
s = 1

# n -- number of jobs
n = int(input('\nEnter the total number of jobs:'))

# p -- matrix of processing times of jobs
p = [int (x) for x in input('\nEnter the processing time for each job:').split()]

# w -- matrix of weights of jobs
w = [int (x) for x in input('\nEnter the weight for each job:').split()]

# P -- partial sum of processing times p
P = [0] * (n+1)
for i in range(1, n+1):
    sum = 0
    for j in range(i):
        sum += p[j]
    P[i] = sum
print ('\nP -- partial sum of processing times p:', P)

# W -- partial sum of weights w
W = [0] * (n+1)
for i in range(1, n+1):
    sum = 0
    for j in range(i):
        sum += w[j]
    W[i] = sum
print ('\nW -- partial sum of weights w:', W)

# C -- matrix of edge costs; C[i,j] -- cost of edge (i,j)
# C[i,j] = (Wn - Wi)(s + Pj - Pi)
C = dict()
print('\nMatrix of edge costs:')
for i in range(n+1):
    for j in range(i+1, n+1):
        C[i,j] = ((W[n] - W[i]) * (s + P[j] - P[i]))
        print ('cost of edge (',i, ',', j, ') :',C[i,j])

# E[l] -- cost of shortest path from 0 to l
# E[l] = min{ E[k] + C[k,l] } with E[0] = 0 and 1 ≤ k ≤ l
E = dict()
E[0] = 0

E_value_coordinates = dict()
# E_value_coordinates[count of E, row number for min value, column number for min value]
E_value_coordinates[0, 0, 0] = 0

for i in range(1, n+1):
    min_value = float('inf')
    min_coordinates = [0,0]
    for j in range(i):
        temp = dict()
        temp[j,i] = E[j] + C[j,i]
        if temp[j,i] < min_value:
            min_value = temp[j,i]
            min_coordinates = [j,i]

    E[i] = min_value
    E_value_coordinates[i, min_coordinates[0], min_coordinates[1]] = min_value

print('\nShortest Path from node 0 to node '+ str(n)+':')
nodes = dict()
# get the start and end nodes of each edge
for key in E_value_coordinates.keys():
    if nodes.get(key[1]) is None:
        nodes[key[1]] = [key[2]]
    else:
        nodes[key[1]].append(key[2])

path = []
for key in nodes.keys():
    if key not in path:
        path.append(key)
    value = nodes[key]
    last_value = value[len(value)-1]
    if last_value:
        if last_value not in path:
            path.append(last_value)

for p in path:
    print(p, end='-->')

print('\n\nCost of shortest path from node 0 to node '+ str(n)+':',E[n])




