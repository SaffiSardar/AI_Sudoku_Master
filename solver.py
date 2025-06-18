import time

def parse_sudoku(puzzle_string):
    return [[int(puzzle_string[i * 9 + j]) for j in range(9)] for i in range(9)]

def board_to_string(board):
    return ''.join(str(num) for row in board for num in row)

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

def count_solutions(board):
    temp_board = [row[:] for row in board]
    solutions = [0]

    def solve_and_count(board):
        if solutions[0] >= 2:
            return
        mrv_cell = find_mrv_cell(board)
        if not mrv_cell:
            solutions[0] += 1
            return
        row, col, options = mrv_cell
        for num in options:
            board[row][col] = num
            solve_and_count(board)
            board[row][col] = 0
            if solutions[0] >= 2:
                return

    solve_and_count(temp_board)
    return solutions[0]

# 🔥 New: solve with timer
def solve_timed(board):
    start = time.perf_counter()
    solve(board)
    end = time.perf_counter()
    return end - start
