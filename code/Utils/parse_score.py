import os
import sys

# Function to parse the score from a file
def parse_score_from_file(filename):
    score = None
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("Score:") or line.startswith("Second best score:"):
                score = float(line.split(":")[1].strip())
                break
    return score

# Function to parse scores from a range of solution files
def parse_scores_from_files(directory, start=1, end=10):
    scores = []
    for i in range(start, end + 1):
        filename = os.path.join(directory, f"solution{i}.txt")
        if os.path.exists(filename):
            score = parse_score_from_file(filename)
            if score is not None:
                scores.append(score)
            else:
                print(f"No score found in {filename}")
        else:
            print(f"{filename} does not exist")
    return scores

# Main execution
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("")
        print("""Usage: python3 parse_score.py <n> <solver>
          <n>: The problem set size.
          <solver>: The problem solver to parse.
          This script expects the following directory structure:
               ../../data/n<n>/solutions/<solver>/solutionX.txt
        \nExample:
        python3 parse_score.py 8 backtrack
        This will parse scores in ../../data/n8/solutions/backtrack/""")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: <n> must be an integer")
        sys.exit(1)
    

    directory = f"../../data/n{n}/solutions/{sys.argv[2]}"
    
    start_file = 1
    end_file = 8
    
    # Ensure the directory exists
    if os.path.isdir(directory):
        scores = parse_scores_from_files(directory, start=start_file, end=end_file)
        print(scores)
    else:
        print(f"The directory {directory} does not exist.")
