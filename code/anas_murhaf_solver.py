import sys
import time
from dwave.embedding.chain_strength import scaled
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
import dwave.inspector
import numpy as np
from plot import plot_solution, plot_problem



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
#np.set_printoptions(threshold=sys.maxsize)
    
lagrange_multiplier = np.max(np.abs(M))

def is_valid_solution(X):
    rows, cols = X.shape
    for i in range(rows):
        count = 0
        for j in range(cols):
            if X[i,j] == 1:
                count += 1
        if not count == 2:
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


n, _ = M.shape

sampler = EmbeddingComposite(DWaveSampler()) # QPU sampler to run in production
t0 = time.perf_counter()
sampleset = sampler.sample_qubo(Q, num_reads=num_samples)
t1 = time.perf_counter()
dwave.inspector.show(sampleset)
have_solution = False
problem_id = sampleset.info['problem_id']
chain_strength = sampleset.info['embedding_context']['chain_strength']

with open(out_file, 'w') as f:
    f.write(f"Problem Id: {problem_id}\n")        # does not depend on sample  
    count = 0
    for e in sampleset.data(sorted_by='energy'):
        sample = e.sample
        energy = e.energy
        num_occurrences = e.num_occurrences
        chain_break_fraction = e.chain_break_fraction
        X = build_solution(sample)
        # if is_valid_solution(X):
        have_solution = True
        score, path = score(M, X)
        f.write(f"Solution:\n")
        f.write(f"{X}\n")
        f.write(f"Score: {score}\n")
        f.write(f"{sample}\n")
        f.write(f"index: {count}\n")
        f.write(f"energy: {energy}\n")
        f.write(f"num_occurrences: {num_occurrences}\n")            
        f.write(f"chain break fraction: {chain_break_fraction}\n")            
        break   # break out of for loop
        count += 1
    f.write(f"chain strength: {chain_strength}\n")  # does not depend on sample
    f.write(f"lagrange multiplier: {lagrange_multiplier}\n")
    f.write(f"Time: {t1-t0:0.4f} s\n")
    if not have_solution:
        # https://docs.ocean.dwavesys.com/en/latest/examples/inspector_graph_partitioning.html
        # this is the overall chain break fraction
        chain_break_fraction = np.sum(sampleset.record.chain_break_fraction)/num_samples
        f.write("did not find any solution\n")
        f.write(f"chain break fraction: {chain_break_fraction}\n")

plot_solution( n, path , M)
plot_problem(M)