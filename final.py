''' Optimal or near optimal solutions to the serial batching problem under weighted average completion '''
# author : Shradha Kapoor
# date : January 30, 2019
# python_version : 3.6


class Batching(object):
    def __init__(self):
        ''' Calculate initial cost matrix, i.e. cost from node 0 to node i'''

        # s -- selection time
        s = 1

        # n -- number of jobs
        n = int(input('\nEnter the total number of jobs:'))
        self.n = n

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
        print('\nInitial Matrix of edge costs:')
        for i in range(n+1):
            for j in range(i+1, n+1):
                C[i,j] = ((W[n] - W[i]) * (s + P[j] - P[i]))
                print ('cost of edge (',i, ',', j, ') :',C[i,j])

        # Path always start from 0
        self.cost_zero_to_i = C

    def dynamic_program(self):
        # matrix to store the minimum value of E in each K
        minimum_E = dict()
        # matrix to store current calculations for E
        current_E = dict()

        for y in range(1, self.n+1):
            minimum_E[1,y] = self.cost_zero_to_i[0,y]

        # iterate to increment number_of_edges(k) by one till k<=n, start with k=2
        for k in range(2, self.n+1):

            # iterate to increment last_node_number(i) by one till i<=n, start with i=2
            for i in range(1, self.n+1):
                # iterate to increment last_but_one_node_number(l) by one till l<=n, start with l=1
                for l in range(1, self.n+1):
                    if i < k or l >= i:
                        current_E[i,l] = float('inf')
                    else:
                        current_E[i,l] = minimum_E[k-1,l] + self.cost_zero_to_i[l,i]

            # add next row to minimum_E matrix
            for y in range(1, self.n+1):
                minimum_E[k, y] = self.find_minimum(current_E, y)

        return minimum_E

    def find_minimum(self,curr_E, row):
        mini = float('inf')
        for i in range(1, self.n+1):
            if curr_E[row, i] < mini:
                mini = curr_E[row, i]

        return mini


batch = Batching()
result = batch.dynamic_program()
print('Minimum E:', result )
