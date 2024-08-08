#!/usr/bin/env python
"""This program implements a backtracking algorithm to solve the Traveling Salesman Problem (TSP).

The algorithm tries every possible path and chooses the one with the minimum cost. 
It recursively explores all possible tours starting from the first city, 
updating the minimum cost whenever a better path is found.

The program takes two inputs:
1. A file containing the pairwise costs as an adjacency matrix.
2. The output file where the solution (minimum cost and corresponding path) will be written.

The program can be run like this:
$ python tsp.py problem.txt solution.txt
"""

import sys

__author__ = "Murhaf Alawir, Anas Alatasi"
__copyright__ = "Global1A1"
__credits__ = ["Murhaf Alawir, Anas Alatasi"]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Murhaf Alawir"
__email__ = "m.alawir@innopolis.university"
__status__ = "Staging"

def read_adjacency_matrix(file_path):
    """Reads an adjacency matrix from a file.

    Args:
        file_path (str): The path to the file containing the adjacency matrix.

    Returns:
        list: A 2D list representing the adjacency matrix.
    """
    with open(file_path, 'r') as file:
        matrix = []
        for line in file:
            row = list(map(int, line.split()))
            matrix.append(row)
    return matrix

def write_output(file_path, min_cost, path):
    """Writes the minimum cost and path to an output file.

    Args:
        file_path (str): The path to the output file.
        min_cost (int): The minimum cost found by the algorithm.
        path (list): The path corresponding to the minimum cost.
    """
    with open(file_path, 'w') as file:
        file.write(f"Score: {min_cost}\n")
        file.write("Path: " + ' -> '.join(map(str, path)) + '\n')

def tsp_backtracking(matrix):
    """Solves the Traveling Salesman Problem using backtracking.

    Args:
        matrix (list): A 2D list representing the adjacency matrix.

    Returns:
        tuple: The minimum cost and the path corresponding to this cost.
    """
    n = len(matrix)
    visited = [False] * n
    min_cost = float('inf')
    best_path = []

    def backtrack(curr_pos, count, cost, path):
        """Recursively explores all possible paths to find the minimum cost.

        Args:
            curr_pos (int): The current position in the path.
            count (int): The number of nodes visited so far.
            cost (int): The current cost of the path.
            path (list): The current path being explored.
        """
        nonlocal min_cost, best_path

        if count == n and matrix[curr_pos][0] > 0:
            total_cost = cost + matrix[curr_pos][0]
            if total_cost < min_cost:
                min_cost = total_cost
                best_path = path[:] + [0]
            return

        for i in range(n):
            if not visited[i] and matrix[curr_pos][i] > 0:
                visited[i] = True
                path.append(i)
                backtrack(i, count + 1, cost + matrix[curr_pos][i], path)
                visited[i] = False
                path.pop()

    visited[0] = True
    backtrack(0, 1, 0, [0])
    return min_cost, best_path

def main(input_file, output_file):
    """Main function to read input, solve the problem, and write the output.

    Args:
        input_file (str): The path to the input file containing the adjacency matrix.
        output_file (str): The path to the output file where the solution will be written.
    """
    matrix = read_adjacency_matrix(input_file)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j > i:
                matrix[i][j] += matrix[j][i]
            else:
                matrix[i][j] = matrix[j][i]
    min_cost, best_path = tsp_backtracking(matrix)
    write_output(output_file, min_cost, best_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tsp.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
