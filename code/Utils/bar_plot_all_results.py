import matplotlib.pyplot as plt
import numpy as np

def plot_results(n, new_backtrack, new_quantum_results, dwave_quantum_results, brute_force_results, opt2_results, old_quantum_results, filename):
    # Problem indices
    problems = np.arange(1, len(new_backtrack) + 1)
    bar_width = 0.15

    # Create figure
    fig, ax = plt.subplots(figsize=(18, 8))

    # Positions for the bars
    r1 = np.arange(len(new_backtrack))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]
    r5 = [x + bar_width for x in r4]
    r6 = [x + bar_width for x in r5]

    # Colors
    colors = ['#BBBBBB', '#ff3333', '#1ED00D', '#5B9ACE', '#9019B9', '#CCCE47']

    # Plotting
    plt.bar(r1, new_backtrack, color=colors[0], width=bar_width, edgecolor='grey', label='New Backtrack')
    plt.bar(r2, new_quantum_results, color=colors[1], width=bar_width, edgecolor='grey', label='New Quantum')
    plt.bar(r3, dwave_quantum_results, color=colors[2], width=bar_width, edgecolor='grey', label='D-Wave Quantum')
    plt.bar(r4, brute_force_results, color=colors[3], width=bar_width, edgecolor='grey', label='Old Brute Force')
    plt.bar(r5, opt2_results, color=colors[4], width=bar_width, edgecolor='grey', label='Old 2-Opt')
    plt.bar(r6, old_quantum_results, color=colors[5], width=bar_width, edgecolor='grey', label='Old Quantum')

    # Adding labels
    plt.xlabel('Problem Number', fontweight='bold', fontsize=14)
    plt.ylabel('Result Value', fontweight='bold', fontsize=14)
    plt.xticks([r + 2.5*bar_width for r in range(len(new_backtrack))], problems, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the plot as a file
    plt.savefig(filename, format='png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()

# Data for n = 8
new_backtrack_8 = [54.0, 54.0, 41.0, 49.0, 40.0, 52.0, 51.0, 47.0]
new_quantum_results_8 = [54.0, 54.0, 41.0, 49.0, 40.0, 52.0, 51.0, 47.0]
dwave_quantum_results_8 = [54.0, 54.0, 41.0, 49.0, 40.0, 52.0, 51.0, 47.0]
brute_force_results_8 = [54, 54, 41, 49, 40, 52, 51, 47]
opt2_results_8 = [54, 54, 44, 49, 40, 52, 59, 50]
old_quantum_results_8 = [61, 68, 53, 55, 54, 58, 63, 59]

# Data for n = 9
new_backtrack_9 = [63.0, 57.0, 54.0, 64.0, 64.0, 54.0, 61.0, 71.0]
new_quantum_results_9 = [63.0, 57.0, 54.0, 64.0, 64.0, 54.0, 61.0, 71.0]
dwave_quantum_results_9 = [63.0, 60.0, 56.0, 64.0, 66.0, 54.0, 61.0, 72.0]
brute_force_results_9 = [67, 58, 56, 65, 66, 57, 62, 72]
opt2_results_9 = [70.0, 57.0, 54.0, 64.0, 64.0, 59.0, 70.0, 71.0]
old_quantum_results_9 = [0, 90, 0, 0, 78, 63, 0, 0]

# Data for n = 10
new_backtrack_10 = [68.0, 56.0, 63.0, 67.0, 67.0, 56.0, 65.0, 63.0]
new_quantum_results_10 = [68.0, 57.0, 63.0, 67.0, 70.0, 56.0, 65.0, 63.0]
dwave_quantum_results_10 = [71.0, 63.0, 67.0, 71.0, 74.0, 61.0, 72.0, 70.0]
brute_force_results_10 = [69.0, 57.0, 64.0, 68.0, 69.0, 57.0, 66.0, 64.0]
opt2_results_10 = [75.0, 59.0, 69.0, 69.0, 69.0, 58.0, 68.0, 65.0]
old_quantum_results_10 = [0, 0, 0, 0, 0, 97, 0, 0]

# Plot and save results for each n
plot_results(8, new_backtrack_8, new_quantum_results_8, dwave_quantum_results_8, brute_force_results_8, opt2_results_8, old_quantum_results_8, 'n8_results.png')
plot_results(9, new_backtrack_9, new_quantum_results_9, dwave_quantum_results_9, brute_force_results_9, opt2_results_9, old_quantum_results_9, 'n9_results.png')
plot_results(10, new_backtrack_10, new_quantum_results_10, dwave_quantum_results_10, brute_force_results_10, opt2_results_10, old_quantum_results_10, 'n10_results.png')
