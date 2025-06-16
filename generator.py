import random
from copy import deepcopy
from solver import solve

# -------- Helpers to convert between string and board -------- #

def string_to_board(puzzle_str):
    return [[int(puzzle_str[i * 9 + j]) for j in range(9)] for i in range(9)]

def board_to_string(board):
    return ''.join(str(num) for row in board for num in row)

# -------- Remove cells to create puzzle -------- #

def remove_cells(board, blanks=40):
    puzzle = [row[:] for row in board]
    removed = 0
    while removed < blanks:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            removed += 1
    return puzzle

# -------- Validate solvability -------- #

def is_solvable(puzzle_board):
    temp = deepcopy(puzzle_board)
    return solve(temp)

# -------- Main Generator Logic -------- #

def generate_puzzle(blanks=40):
    with open("sudoku_solutions.txt", "r") as f:
        all_solutions = f.read().splitlines()

    while True:
        solution_str = random.choice(all_solutions)
        solution_board = string_to_board(solution_str)
        puzzle_board = remove_cells(solution_board, blanks=blanks)

        if is_solvable(puzzle_board):
            return puzzle_board, solution_board

# -------- Save and Display Puzzle -------- #

def save_puzzle(puzzle_board, solution_board):
    with open("generated_puzzles.txt", "a") as p_file, open("generated_solutions.txt", "a") as s_file:
        p_file.write(board_to_string(puzzle_board) + "\n")
        s_file.write(board_to_string(solution_board) + "\n")

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# -------- Run Generator -------- #

if __name__ == "__main__":
    puzzle, solution = generate_puzzle(blanks=40)

    print("\n                      Generated Sudoku Puzzle:\n")
    print_board(puzzle)

    print("\n                      Corresponding Solution:\n")
    print_board(solution)

    save_puzzle(puzzle, solution)
