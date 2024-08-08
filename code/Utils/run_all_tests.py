#!/usr/bin/env python
"""This script runs a solver script on all problem files in a specified directory and stores the solutions in another directory.

Usage:
    python3 run_all_tests.py <n>
    
Arguments:
    <n> (int): The problem set size, which determines the directory structure for problems and solutions.

Directory Structure:
    The script expects the following structure:
        ../../data/n<n>/problems/problemX.txt
        ../../data/n<n>/solutions/eqats_hqpu_solutions/solutionX.txt
    where <n> is the problem size and X is the problem number.

Example:
    python3 run_all_tests.py 8
    This will process problems in ../../data/n8/problems/ and store solutions in ../../data/n8/solutions/eqats_hqpu_solutions/
"""

import os
import subprocess
import sys

def run_solver_on_problems(problem_dir, solution_dir, solver_script):
    """Runs the solver script on all problem files in the problem directory and saves the results to the solution directory.

    Args:
        problem_dir (str): Directory containing problem files.
        solution_dir (str): Directory where solution files will be saved.
        solver_script (str): Path to the solver script.

    Creates:
        Solution directory if it does not exist.
        Runs the solver script for each problem file and saves the output to the corresponding solution file.
    """
    # Create the solution directory if it doesn't exist
    if not os.path.exists(solution_dir):
        os.makedirs(solution_dir)
    
    # Iterate over all problem files in the problem directory
    for filename in os.listdir(problem_dir):
        if filename.startswith("problem") and filename.endswith(".txt"):
            problem_path = os.path.join(problem_dir, filename)
            problem_number = filename.replace("problem", "").replace(".txt", "")
            solution_filename = f"solution{problem_number}.txt"
            solution_path = os.path.join(solution_dir, solution_filename)
            
            # Run the solver script
            try:
                subprocess.run(["python3", solver_script, problem_path, solution_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running solver on {problem_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage: python3 run_all_tests.py <n>")
        print("  <n>: The problem set size.")
        print("This script expects the following directory structure:")
        print("     ../../data/n<n>/problems/problemX.txt")
        print("     ../../data/n<n>/solutions/eqats_hqpu_solutions/solutionX.txt")
        print("\nExample:")
        print("python3 run_all_tests.py 8")
        print("This will process problems in ../../data/n8/problems/ and store solutions in ../../data/n8/solutions/eqats_hqpu_solutions/")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: <n> must be an integer")
        sys.exit(1)
    
    # Define the directories and solver script path
    problem_directory = f"../../data/n{n}/problems"
    solution_directory = f"../../data/n{n}/solutions/eqats_hqpu_solutions"
    solver_script_path = "../Global1A1_Solvers/eqats_solver.py"
    
    # Check if the problem directory exists
    if not os.path.exists(problem_directory):
        print(f"Error: Problem directory {problem_directory} does not exist")
        sys.exit(1)

    # Run the solver on all problems
    run_solver_on_problems(problem_directory, solution_directory, solver_script_path)
