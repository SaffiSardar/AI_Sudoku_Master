# evaluate_solver.py

from solver import solve, parse_sudoku
from tqdm import tqdm
import time

# File paths
puzzles_path = "sudoku_puzzles.txt"
solutions_path = "sudoku_solutions.txt"

# Read data
with open(puzzles_path, 'r') as f:
    puzzles = [line.strip() for line in f.readlines()]

with open(solutions_path, 'r') as f:
    solutions = [line.strip() for line in f.readlines()]

# Accuracy calculation
correct = 0
total = len(puzzles)
start = time.time()

# Loop with progress bar
for i in tqdm(range(total), desc="Evaluating", unit="puzzle"):
    puzzle_str = puzzles[i]
    expected_solution_str = solutions[i]

    board = parse_sudoku(puzzle_str)
    solved = solve(board)

    if not solved:
        continue  # skip unsolved

    result_str = ''.join(str(num) for row in board for num in row)

    if result_str == expected_solution_str:
        correct += 1

accuracy = (correct / total) * 100
end = time.time()

# Results
print(f"\nAccuracy: {accuracy:.2f}%")
print(f"Correct: {correct} / {total}")
print(f"Time taken: {end - start:.2f} seconds")
