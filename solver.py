# solver.py

def parse_sudoku(puzzle_string):
    return [[int(puzzle_string[i * 9 + j]) for j in range(9)] for i in range(9)]

def valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def get_candidates(board, row, col):
    return [num for num in range(1, 10) if valid(board, row, col, num)]

def find_mrv_cell(board):
    min_options = 10
    best_cell = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                options = get_candidates(board, row, col)
                if len(options) < min_options:
                    min_options = len(options)
                    best_cell = (row, col, options)
                    if min_options == 1:
                        return best_cell
    return best_cell

def solve(board):
    mrv_cell = find_mrv_cell(board)
    if not mrv_cell:
        return True
    row, col, options = mrv_cell
    for num in options:
        board[row][col] = num
        if solve(board):
            return True
        board[row][col] = 0
    return False

# Optional: allow running this file directly for a test
"""
if __name__ == "__main__":
    puzzle_string = "800000000003600000070090020050007000000045700000100030001000068008500010090000400"
    board = parse_sudoku(puzzle_string)

    if solve(board):
        for row in board:
            print(" ".join(str(num) for num in row))
    else:
        print("No solution found.")
    """
