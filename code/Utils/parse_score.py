import os

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
    # Allow user to input the directory path
    directory = input("Enter the path to the directory containing the solution files: ")
    
    start_file = 1
    end_file = 8  # Adjust this to the number of files you want to parse
    
    # Ensure the directory exists
    if os.path.isdir(directory):
        scores = parse_scores_from_files(directory, start=start_file, end=end_file)
        print(scores)
    else:
        print(f"The directory {directory} does not exist.")
