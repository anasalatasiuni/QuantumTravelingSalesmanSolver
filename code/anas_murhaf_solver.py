import sys
import time
from dwave.system.composites import EmbeddingComposite
from dwave.system import DWaveSampler
import dwave.inspector

import numpy as np
from plot import plot_solution



in_file = sys.argv[1]
out_file = sys.argv[2]
num_samples = 1000

M0 = np.loadtxt(in_file)
M = np.loadtxt(in_file)

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        M[i, j] += M0[j, i]


_lambda = np.max(np.abs(M))*2

def build_objective_matrix():
    n, _ = M.shape
    n = n-1
    m = int(n*n)
    Q = np.zeros((m,m))
    for i in range(m):
        Q[i,i] =  2 * -_lambda
        city_i = i // n + 1
        pos_i = i % n
        if pos_i == 0:      # Edge with the first node
            Q[i,i] += M[city_i, 0]
        if pos_i == n-1:    # Edge with the first node
            Q[i,i] += M[city_i, 0]
        k = i + 1
        while (k % n) != 0:
            Q[i,k] = 2 * _lambda
            if pos_i == 0:      # Edge with the first node
                Q[i,k] += M[city_i, 0]
        
            if pos_i == n-1:    # Edge with the first node
                Q[i,k] += M[city_i, 0]
            k += 1
    for i in range(m):
        for j in range(i + 1, m):

            city_i = i // n + 1
            pos_i = i % n
            city_j = j // n + 1
            pos_j = j % n

            if city_i == city_j:
                continue
            elif pos_i == pos_j-1 or pos_i == pos_j+1:
                Q[i,j] = M[city_i,city_j]
            elif pos_i == pos_j:
                Q[i,j] = 2 * _lambda
    return Q


Q = build_objective_matrix()
np.set_printoptions(threshold=sys.maxsize)
with open("Q.txt", 'w') as f:
    f.write(f"{Q}\n")

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
    
def build_solution(sample):
    n, _ = M.shape # this will use the global M variable
    m = len(sample)
    assert m == int((n-1)*(n-1))
    X = np.zeros((n,n))
    k = 0
    X[0,0] = 1
    for i in range(1,n):
        for j in range(1,n):
            X[i,j] = sample[k]
            k += 1
    return X

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


def solve(best_energy):
    n, _ = M.shape
    sampler = EmbeddingComposite(DWaveSampler())
    t0 = time.perf_counter()
    sampleset = sampler.sample_qubo(Q, num_reads=num_samples)
    t1 = time.perf_counter()
    dwave.inspector.show(sampleset)
    problem_id = sampleset.info['problem_id']

    for e in sampleset.data(sorted_by='energy'):
        sample = e.sample
        energy = e.energy
        num_occurrences = e.num_occurrences
        chain_break_fraction = e.chain_break_fraction
        
        if best_energy <= energy:
            return best_energy

        with open(out_file, 'w') as f:
            X = build_solution(sample)
            if is_valid_solution(X):
                f.write(f"Problem Id: {problem_id}\n")
                best_energy = energy
                cost, path = score(M, X)
                f.write(f"Solution:\n")
                f.write(f"{X}\n")
                f.write(f"Score: {cost}\n")
                f.write(f"{sample}\n")
                f.write(f"energy: {energy}\n")
                f.write(f"num_occurrences: {num_occurrences}\n")            
                f.write(f"chain break fraction: {chain_break_fraction}\n")            
                f.write(f"Time: {t1-t0:0.4f} s\n")
                break
            
    return best_energy

best_energy = 1e9
for _ in range(4):
    best_energy = solve(best_energy)