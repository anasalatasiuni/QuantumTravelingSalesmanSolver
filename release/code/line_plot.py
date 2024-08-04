#!/usr/bin/env python
"""This file contains the code used to generate figure 1 in the paper.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

__author__ = "Siddharth Jain"
__copyright__ = "Copyright 2021, Johnson & Johnson"
__credits__ = ["Siddharth Jain"]
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "Siddharth Jain"
__email__ = "sjain68@its.jnj.com"
__status__ = "Production"

# prerequisite: need to install:
# conda install -c anaconda pyqt
# see https://gist.github.com/siddjain/44c70083a72b888c64033ff51de755af
matplotlib.use("Qt5Agg")
file = '../data/n8/solutions/brute-force/scores1.txt'
M = np.loadtxt(file)
fig, ax = plt.subplots()
ax.plot(M[:,0], M[:,1])
ax.set_xlabel('combinations', fontsize=16)
ax.set_ylabel(r'$\sum M .* X$', fontsize=16)
fig.show()
input("Press ENTER to exit")
