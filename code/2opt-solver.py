#!/usr/bin/env python
"""This program implements the 2-opt solver technique to solve the TSP
(Traveling Salesman Problem)

The algorithm is simple. We start with initial configuration. Then we swap
two nodes and check if the new configuration has a lower cost. If so,
we keep this swap and repeat recursively until there is no improvement in the 
cost function.

The program takes two inputs:
1. A file containing the pairwise costs as a matrix. These can be found in data.zip
2. The output file containing the solution found by this method

The program can be run like this:
$ python 2opt-solver.py problem.txt solution.txt
"""

import numpy as np
import sys
import time
import itertools

__author__ = "Siddharth Jain"
__copyright__ = "Copyright 2021, Johnson & Johnson"
__credits__ = ["Siddharth Jain"]
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "Siddharth Jain"
__email__ = "sjain68@its.jnj.com"
__status__ = "Production"

def ring(nodes):
    """ create a ring from input list that tells which node is connect to which. The input list should be thought of as a ring or cycle. """
    n = len(nodes)
    A = np.zeros((n,n))
    for i in range(n):
        j = (i + 1) % n
        u = nodes[i]
        v = nodes[j]
        A[u,v] = A[v,u] = 1 # connect nodes[i] to nodes[j]
    return A

def score(M, X):
    return np.sum(np.multiply(M, X))

def solve(M):
    """ solve traveling salesman problem given matrix of distances or costs """
    n, _ = M.shape
    nodes = list(range(n))
    X = ring(nodes)
    best_matrix = X
    best_score = score(M, X)
    finish = False
    steps = 1
    while not finish:
        finish = True
        for pair in itertools.combinations(nodes, 2):
            copy = nodes.copy()
            i = pair[0]
            j = pair[1]
            # swap i and j. this works in python
            copy[i], copy[j] = copy[j], copy[i]
            # compute new score
            X = ring(copy)
            f = score(M, X)
            steps += 1
            if f < best_score:
                best_score = f
                best_matrix = X
                nodes = copy # update reference
                finish = False # this will cause while loop to execute again
                break # break out of for loop     
    return best_matrix, best_score, steps

in_file = sys.argv[1]
out_file = sys.argv[2]
# the matrix of pairwise costs. this need not be a symmetric matrix but the diagonal entries are ignored
# and assumed to be zero (don't care)
M = np.loadtxt(in_file)
tic = time.perf_counter()
X, best_score, steps = solve(M)
toc = time.perf_counter()

with open(out_file, 'w') as f:
    f.write("Score: {0}\n".format(best_score))
    f.write("Solution:\n {0}\n".format(X))
    f.write("Steps: {0}\n".format(steps))
    f.write("Time: {0:0.4f} s\n".format(toc - tic))
