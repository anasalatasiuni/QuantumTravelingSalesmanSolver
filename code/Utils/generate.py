#!/usr/bin/env python
"""Code to generate TSP problem sets.
"""

import random
import numpy as np
import sys

__author__ = "Siddharth Jain"
__copyright__ = "Copyright 2021, Johnson & Johnson"
__credits__ = ["Siddharth Jain"]
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "Siddharth Jain"
__email__ = "sjain68@its.jnj.com"
__status__ = "Production"

n = int(sys.argv[1])
file = sys.argv[2]
M = np.zeros((n,n))
for i in range(0, n):
    for j in range(0, n):
        if i != j:
            M[i, j] = random.randint(1, n)   

np.savetxt(file, M, fmt='%d')

# to load the file:
# M=np.loadtxt("test.csv")
