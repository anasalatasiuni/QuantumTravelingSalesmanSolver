import matplotlib.pyplot as plt
import numpy as np

# Sample data: Replace these with your actual arrays
brute_force_results = [54, 54, 41, 49, 40, 52, 51, 47]
opt2_results = [54, 54, 44, 49, 40, 52, 59, 50]
qpu_original_results = [61, 68, 53, 55, 54, 58, 63, 59]
qpu_our_results = [54, 56, 46, 50, 40, 53, 53, 50]

# Combine results for each algorithm
data_for_boxplot = [brute_force_results, opt2_results, qpu_original_results, qpu_our_results]

# Labels for the box plots
labels = ['Brute Force', '2-Opt', 'QPU Jain et al. (2021)', 'QPU Our Proposed Solution']

# Create a color scheme
box_colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow']

plt.figure(figsize=(12, 6))

# Create the box plots
box = plt.boxplot(data_for_boxplot, patch_artist=True)

# Customizing the box plot colors
for patch, color in zip(box['boxes'], box_colors):
    patch.set_facecolor(color)

# Customizing other parts of the box plot
for whisker in box['whiskers']:
    whisker.set(color='black', linewidth=1.5)
for cap in box['caps']:
    cap.set(color='black', linewidth=1.5)
for median in box['medians']:
    median.set(color='red', linewidth=2)

# Customizing the plot
plt.xlabel('Algorithm', fontweight='bold')
plt.ylabel('Score', fontweight='bold')
plt.xticks(ticks=[1, 2, 3, 4], labels=labels)
plt.grid(True)

# Add a legend
patches = [plt.plot([], [], marker="s", ms=10, ls="", mec=None, color=color, 
            label="{:s}".format(label))[0] for color, label in zip(box_colors, labels)]
plt.legend(handles=patches, loc='upper left')

plt.savefig('algorithm_results_comparison_for_n8.png', format='png', dpi=300)
#plt.show()
