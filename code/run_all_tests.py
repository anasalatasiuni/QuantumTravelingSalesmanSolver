import os
import subprocess
import sys

def run_solver_on_problems(problem_dir, solution_dir, solver_script):
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
            subprocess.run(["python3", solver_script, problem_path, solution_path])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""Usage: python3 run_anas_murhaf_solutions.py <n>
          <n>: The problem set size. This script expects the following directory structure:
               ../data/n<n>/problems/problemX.txt
               ../data/n<n>/solutions/anas_murhaf_solutions/solutionX.txt
        \nExample:
        python3 run_anas_murhaf_solutions.py 8
        This will process problems in ../data/n8/problems/ and store solutions in ../data/n8/solutions/anas_murhaf_solutions/""")
        sys.exit(1)
        
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: <n> must be an integer")
        sys.exit(1)

    # Define the directories and solver script path
    problem_directory = f"../data/n{n}/problems"
    solution_directory = f"../data/n{n}/solutions/anas_murhaf_solutions"
    solver_script_path = "anas_murhaf_solver.py"
    
    # Check if the problem directory exists
    if not os.path.exists(problem_directory):
        print(f"Error: Problem directory {problem_directory} does not exist")
        sys.exit(1)

    # Run the solver on all problems
    run_solver_on_problems(problem_directory, solution_directory, solver_script_path)
