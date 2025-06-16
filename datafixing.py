import csv

# Input CSV filename
input_csv = "sudoku.csv"

# Output filenames
puzzles_file = "sudoku_puzzles.txt"
solutions_file = "sudoku_solutions.txt"

# Open the input CSV and the two output files
with open(input_csv, 'r') as csv_file, \
     open(puzzles_file, 'w') as puzzle_out, \
     open(solutions_file, 'w') as solution_out:

    reader = csv.DictReader(csv_file)

    for row in reader:
        puzzle = row['quizzes'].strip()
        solution = row['solutions'].strip()

        if len(puzzle) == 81 and len(solution) == 81:
            puzzle_out.write(puzzle + '\n')
            solution_out.write(solution + '\n')
