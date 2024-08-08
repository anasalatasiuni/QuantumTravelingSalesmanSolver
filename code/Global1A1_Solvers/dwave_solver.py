from dwave_networkx import traveling_salesperson_qubo
import networkx as nx
from dwave.system import LeapHybridSampler
import sys
import numpy as np


def score(M, X):
    n, _ = M.shape
    last = -1
    ans = 0
    first = 0
    path = []
    for j in range(n):
        for i in range(n):
            if X[i,j] == 1:
                if last == -1:
                    last = i
                    first = i
                    path.append(first)
                    break
                ans += M[last,i]
                last = i
                path.append(last)
                break
    ans += M[last,first]
    path.append(first)
    return ans, path


def is_valid_solution(X):
    n, _ = X.shape
    for i in range(n):
        count = 0
        for j in range(n):
            if X[i,j] == 1:
                count += 1
        if count != 1:
            return False
    return True

in_file = sys.argv[1]
out_file = sys.argv[2]
num_samples = 1000

M0 = np.loadtxt(in_file)
M = np.loadtxt(in_file)

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        M[i, j] += M0[j, i]

G = nx.from_numpy_array(M)

new_q = traveling_salesperson_qubo(G)


sampler = LeapHybridSampler()
sampleset = sampler.sample_qubo(new_q,time_limit=3)

first = sampleset.first

problem_id = sampleset.info['problem_id']

e = first.sample.values()

    
def _build_solution(sample):
    n, _ = M.shape
    m = len(sample)
    assert m == int(n*n)
    X = np.zeros((n,n))
    i=0
    j=0
    for x in sample:
        X[i,j] = x
        j += 1
        if j == n:
            j = 0
            i += 1
    return X

X = _build_solution(e)
if is_valid_solution(X):
    cost, path = score(M, X)
    with open(out_file, 'w') as f:
        f.write(f"{X}\n")
        f.write(f"Score: {cost}\n")
        f.write(f"path: {path}\n")