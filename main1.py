''' Optimal or near optimal solutions to the serial batching problem under weighted average completion '''
# author : Shradha Kapoor
# date : September 6, 2018
# python_version : 3.6


class SchedulingJobs(object):
    def __init__(self):
        # s -- selection time
        self.s = 1

        # n -- number of jobs
        self.n = int( input( '\nEnter the total number of jobs:' ) )
        if self.n == 0:
            print('Please enter a valid number of jobs.')
            exit(0)

        # p -- matrix of processing times of jobs
        self.p = [int( x ) for x in input( '\nEnter the processing time for each job:' ).split()]
        if len(self.p) != self.n:
            print('Please enter one processing time for one job.')
            exit(0)

        # w -- matrix of waiting times of jobs
        self.w = [int( x ) for x in input( '\nEnter the waiting time for each job:' ).split()]
        if len(self.w) != self.n:
            print('Please enter one waiting time for one job.')
            exit(0)

    # P -- partial sum of processing times p
    def partial_sum_processing_times(self, p):
        P = [0] * (self.n + 1)
        for i in range( 1, self.n + 1 ):
            sum = 0
            for j in range( i ):
                sum += p[j]
            P[i] = sum

        return P

    # W -- partial sum of waiting times w
    def partial_sum_waiting_times( self, w ):
        W = [0] * (self.n + 1)
        for i in range( 1, self.n + 1 ):
            sum = 0
            for j in range( i ):
                sum += w[j]
            W[i] = sum

        return W

    # C -- matrix of edge costs; C[i,j] -- cost of edge (i,j)
    # C[i,j] = (Wn - Wi)(s + Pj - Pi)
    def matrix_edge_costs( self, P, W ):
        C = dict()
        for i in range( self.n + 1 ):
            for j in range( i + 1, self.n + 1 ):
                C[i, j] = ((W[self.n] - W[i]) * (self.s + P[j] - P[i]))

        return C

    # E[l] -- cost of shortest path from 0 to l
    # E[l] = min{ E[k] + C[k,l] } with E[0] = 0 and 1 ≤ k ≤ l
    def cost_shortest_path( self, C ):
        E = dict()
        E[0] = 0

        E_value_coordinates = dict()
        # E_value_coordinates[count of E, row number for min value, column number for min value]
        E_value_coordinates[0, 0, 0] = 0

        for i in range( 1, self.n + 1 ):
            min_value = float( 'inf' )
            min_coordinates = [0, 0]
            for j in range( i ):
                temp = dict()
                temp[j, i] = E[j] + C[j, i]
                if temp[j, i] < min_value:
                    min_value = temp[j, i]
                    min_coordinates = [j, i]

            E[i] = min_value
            E_value_coordinates[i, min_coordinates[0], min_coordinates[1]] = min_value

        return E_value_coordinates, E

    # print shortest path from start to end node
    def print_shortest_path_from_start_to_end( self, E_value_coordinates, E):
        nodes = dict()
        # get the start and end nodes of each edge
        for key in E_value_coordinates.keys():
            if nodes.get( key[1] ) is None:
                nodes[key[1]] = [key[2]]
            else:
                nodes[key[1]].append( key[2] )

        path = []
        for key in nodes.keys():
            if key not in path:
                path.append( key )
            value = nodes[key]
            last_value = value[len( value ) - 1]
            if last_value:
                if last_value not in path:
                    path.append( last_value )

        return path

    # All permutations of given list of jobs
    def all_permutations_of_jobs( self, p, w ):
        lst = []
        # list of jobs as (job number, it's processing time, it's waiting time)
        for i in range(self.n):
            lst.append((i, p[i], w[i]))

        return self._all_permutations_of_jobs(lst)

    # recursive function to generate all permutations of the jobs
    def _all_permutations_of_jobs( self, lst ):
        # no permutations possible in empty lst
        if len( lst ) == 0:
            return []

        # only one permutation possible in lst with only one element
        if len( lst ) == 1:
            return [lst]

        # permutations for lst if there are more than 1 jobs
        l = []  # empty list that will store current permutation

        # Iterate the input(lst) to calculate the permutation
        for i in range( len( lst ) ):
            m = lst[i]

            # Extract lst[i] from the lst. remaining_list is remaining list
            remaining_list = lst[:i] + lst[i + 1:]

            # Generating all permutations where lst[i] is the first element
            for p in self._all_permutations_of_jobs(remaining_list):
                l.append( [m] + p )

        return l


if __name__ == "__main__":
    j = SchedulingJobs()

    all_permutations = j.all_permutations_of_jobs(j.p,j.w)
    all_costs_shortest_paths = []
    all_shortest_paths = []

    # iterate over each list of permutations
    for i in range(len(all_permutations)):
        lst = all_permutations[i]

        # form the list of processing times in the same order as the permutation
        p = []
        for k in range(j.n): p.append(lst[k][1])
        P = j.partial_sum_processing_times(p)

        # form the list of waiting times in the same order as the permutation
        w = []
        for k in range( j.n ): w.append( lst[k][2] )
        W = j.partial_sum_waiting_times(w)

        C = j.matrix_edge_costs(P, W)
        E_value_coordinates, E = j.cost_shortest_path(C)
        cost_shortest_path = E[j.n]
        shortest_path = j.print_shortest_path_from_start_to_end(E_value_coordinates, E)

        all_costs_shortest_paths.append(cost_shortest_path)
        all_shortest_paths.append(shortest_path)

    # print the details about the permutation that gives smallest cost among all shortest paths
    min_cost = float('inf')
    min_cost_index = None
    for i in range(len(all_costs_shortest_paths)):
        if all_costs_shortest_paths[i] < min_cost:
            min_cost_index = i
            min_cost = all_costs_shortest_paths[i]

    print('\nNumber of permutations generated to find this shortest path:', len(all_costs_shortest_paths))

    print( '\nShortest Path from node 0 to node ' + str( j.n ) + ':' )
    for p in all_shortest_paths[min_cost_index]:
            print( p, end='-->' )

    print( '\n\nCost of shortest path from node 0 to node ' + str( j.n ) + ':',
           all_costs_shortest_paths[min_cost_index] )

