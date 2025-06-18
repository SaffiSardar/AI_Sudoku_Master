import random
import copy
import time
from solver import solve, count_solutions, board_to_string  # Import from solver.py

# Generate a full valid Sudoku grid
def generate_full_grid():
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill diagonal 3x3 boxes (independent)
    for box in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        idx = 0
        for i in range(box, box + 3):
            for j in range(box, box + 3):
                board[i][j] = nums[idx]
                idx += 1
    
    # Solve the rest
    solve(board)
    return board

# Remove cells to create a puzzle with a unique solution
def remove_cells(board, blanks=40):
    puzzle = copy.deepcopy(board)
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    removed = 0
    
    for r, c in cells:
        if removed >= blanks:
            break
        
        if puzzle[r][c] != 0:
            temp = puzzle[r][c]
            puzzle[r][c] = 0
            # Check if puzzle still has exactly one solution
            if count_solutions(puzzle) != 1:
                puzzle[r][c] = temp  # Restore if not unique
            else:
                removed += 1
    return puzzle

# Save puzzle and solution
def save_puzzle(puzzle_board, solution_board):
    with open("generated_puzzles.txt", "a") as p_file, open("generated_solutions.txt", "a") as s_file:
        p_file.write(board_to_string(puzzle_board) + "\n")
        s_file.write(board_to_string(solution_board) + "\n")

# Display board
def print_board(board):
    for i, row in enumerate(board):
        if i > 0 and i % 3 == 0:
            print("- - - - - - - - - - - -")
        for j, num in enumerate(row):
            if j > 0 and j % 3 == 0:
                print("|", end=" ")
            print(str(num) if num != 0 else ".", end=" ")
        print()
    print()

# Main generator function
def generate_puzzle(blanks=40):
    # Generate a full grid
    solution_board = generate_full_grid()
    
    # Remove cells to create puzzle
    puzzle_board = remove_cells(solution_board, blanks)
    
    return puzzle_board, solution_board

# Run the generator
if __name__ == "__main__":
    start_time = time.time()
    puzzle, solution = generate_puzzle(blanks=40)
    
    print("\nGenerated Sudoku Puzzle:\n")
    print_board(puzzle)
    
    print("\nCorresponding Solution:\n")
    print_board(solution)
    
    save_puzzle(puzzle, solution)
    
    print(f"\nTime taken: {time.time() - start_time:.2f} seconds")