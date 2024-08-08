#!/usr/bin/env python
"""This script generates a bar plot comparing the performance of different algorithms for solving the Traveling Salesman Problem (TSP).

The plot compares the results of various algorithms including Brute Force, 2-Opt, and Quantum Processing Units (QPU) based methods. 
It visualizes the results for a set of problem instances and saves the plot as a PNG file.

The script uses Matplotlib and NumPy for plotting and data handling.

The `plot_algorithm_comparison` function can be used as follows:
1. `plot_algorithm_comparison(brute_force_results, opt2_results, qpu_original_results, qpu_our_results, filename)` - Plots and saves a comparison of algorithm results.

Example usage:
$ python plot_algorithm_comparison.py
"""

import matplotlib.pyplot as plt
import numpy as np

__author__ = "Murhaf Alawir, Anas Alatasi"
__copyright__ = "Global1A1"
__credits__ = ["Murhaf Alawir", "Anas Alatasi"]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Murhaf Alawir"
__email__ = "m.alawir@innopolis.university"
__status__ = "Staging"

def plot_algorithm_comparison(brute_force_results, opt2_results, qpu_original_results, qpu_our_results, filename):
    """Plots a comparison of algorithm results for the Traveling Salesman Problem (TSP).

    This function generates a bar plot comparing the performance of various TSP algorithms across different problem instances.
    It saves the plot as a PNG file with a specified filename.

    Args:
        brute_force_results (list): Results of the Brute Force algorithm.
        opt2_results (list): Results of the 2-Opt algorithm.
        qpu_original_results (list): Results of the original Quantum Processing Unit (QPU) algorithm.
        qpu_our_results (list): Results of the customized Quantum Processing Unit (QPU) algorithm.
        filename (str): The filename for saving the plot.

    Saves:
        filename: A bar plot comparing the results of different TSP algorithms.
    """
    # Sample data: Replace these with your actual arrays
    # brute_force_results = [100, 200, 150, 300, 250, 400, 350, 450]
    # opt2_results = [95, 190, 145, 290, 240, 390, 345, 440]
    # qpu_original_results = [105, 210, 155, 310, 260, 410, 360, 460]
    # qpu_our_results = [90, 185, 140, 285, 235, 385, 335, 430]

    # Problem indices
    problems = np.arange(1, len(brute_force_results) + 1)
    bar_width = 0.2

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))

    # Positions for the bars
    r1 = np.arange(len(brute_force_results))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    # Colors
    colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

    # Plotting
    plt.bar(r1, brute_force_results, color=colors[0], width=bar_width, edgecolor='grey', label='Brute Force')
    plt.bar(r2, opt2_results, color=colors[1], width=bar_width, edgecolor='grey', label='2-Opt')
    plt.bar(r3, qpu_original_results, color=colors[2], width=bar_width, edgecolor='grey', label='QPU Original')
    plt.bar(r4, qpu_our_results, color=colors[3], width=bar_width, edgecolor='grey', label='QPU Our Solution')

    # Adding labels
    plt.xlabel('Problem Number', fontweight='bold', fontsize=14)
    plt.ylabel('Result Value', fontweight='bold', fontsize=14)
    plt.xticks([r + 1.5*bar_width for r in range(len(brute_force_results))], problems, fontsize=12)
    plt.yticks(fontsize=12)
    plt.title('Algorithm Results Comparison for Each Problem', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the plot as a file
    plt.savefig(filename, format='png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()

# Sample data (replace these with your actual data)
brute_force_results = [100, 200, 150, 300, 250, 400, 350, 450]
opt2_results = [95, 190, 145, 290, 240, 390, 345, 440]
qpu_original_results = [105, 210, 155, 310, 260, 410, 360, 460]
qpu_our_results = [90, 185, 140, 285, 235, 385, 335, 430]

# Plot and save the results
plot_algorithm_comparison(brute_force_results, opt2_results, qpu_original_results, qpu_our_results, 'algorithm_results_comparison.png')
