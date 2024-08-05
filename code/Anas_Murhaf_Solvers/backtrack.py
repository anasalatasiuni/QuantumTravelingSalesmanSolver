import sys

def read_adjacency_matrix(file_path):
    with open(file_path, 'r') as file:
        matrix = []
        for line in file:
            row = list(map(int, line.split()))
            matrix.append(row)
    return matrix

def write_output(file_path, min_cost, path):
    with open(file_path, 'w') as file:
        file.write(f"Score: {min_cost}\n")
        file.write("Path: " + ' -> '.join(map(str, path)) + '\n')

def tsp_backtracking(matrix):
    n = len(matrix)
    visited = [False] * n
    min_cost = float('inf')
    best_path = []

    def backtrack(curr_pos, count, cost, path):
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
    matrix = read_adjacency_matrix(input_file)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if j>i:
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
