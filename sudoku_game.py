import pygame
import time
from solver import solve, parse_sudoku, board_to_string
from generator import generate_puzzle, measure_difficulty_time  # ✅ Updated import

# Initialize Pygame
pygame.init()
FPS = 60

# Fixed window size
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Master")

# Colors
DARK_GRAY = (30, 30, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEAL = (0, 128, 128)
GLOW_TEAL = (0, 180, 180)
LIGHT_YELLOW = (255, 255, 204)
RED = (200, 50, 50)
NEUMORPHIC_LIGHT = (60, 60, 60)
NEUMORPHIC_DARK = (0, 0, 0)

# Font
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# Scaling factors
GRID_WIDTH = 360
BUTTON_WIDTH = 180
CELL_SIZE = GRID_WIDTH // 9
GRID_X = 220
GRID_Y = 100
BUTTON_Y_START = 100
BUTTON_SPACING = 50

# Game state
grid = [[0 for _ in range(9)] for _ in range(9)]
selected_cell = None
move_count = 0
start_time = time.time()
paused = False
hint_text = "Hint: everything is well"
status_text = "Time: 00:00:00"
difficulty_text = "Difficulty: Unknown"
invalid_cell = None
clock = pygame.time.Clock()

def draw_background():
    for y in range(HEIGHT):
        r = 30 + (30 * y // HEIGHT)
        g = 30 + (30 * y // HEIGHT)
        b = 30 + (30 * y // HEIGHT)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, (r + 10, g + 10, b + 10), (x, y, 10, 10), 1)

def draw_title():
    title_surface = title_font.render("Sudoku Master", True, WHITE)
    pygame.draw.rect(screen, (0, 50, 100), (0, 0, WIDTH, 80))
    for offset in range(5, 0, -1):
        glow = title_surface.copy()
        glow.fill((0, 50, 100, 50 // offset), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(glow, (WIDTH // 2 - title_surface.get_width() // 2 + offset, 20 + offset))
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 20))

def draw_grid():
    pygame.draw.rect(screen, (100, 100, 120, 128), (GRID_X - 5, GRID_Y - 5, GRID_WIDTH + 10, GRID_WIDTH + 10))
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, TEAL, (GRID_X, GRID_Y + i * CELL_SIZE), (GRID_X + GRID_WIDTH, GRID_Y + i * CELL_SIZE), thickness)
        if thickness == 4:
            pygame.draw.line(screen, GLOW_TEAL, (GRID_X, GRID_Y + i * CELL_SIZE), (GRID_X + GRID_WIDTH, GRID_Y + i * CELL_SIZE), 1)
        pygame.draw.line(screen, TEAL, (GRID_X + i * CELL_SIZE, GRID_Y), (GRID_X + i * CELL_SIZE, GRID_Y + GRID_WIDTH), thickness)
        if thickness == 4:
            pygame.draw.line(screen, GLOW_TEAL, (GRID_X + i * CELL_SIZE, GRID_Y), (GRID_X + i * CELL_SIZE, GRID_Y + GRID_WIDTH), 1)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, WHITE)
                screen.blit(text, (GRID_X + 5 + j * CELL_SIZE, GRID_Y + 5 + i * CELL_SIZE))

def get_cell_from_pos(pos):
    x, y = pos
    if GRID_X <= x <= GRID_X + GRID_WIDTH and GRID_Y <= y <= GRID_Y + GRID_WIDTH:
        col = (x - GRID_X) // CELL_SIZE
        row = (y - GRID_Y) // CELL_SIZE
        return row, col
    return None

def draw_buttons():
    buttons = [
        ("Pause", 20, BUTTON_Y_START, BUTTON_WIDTH - 40, 40),
        ("Resume", 20, BUTTON_Y_START + BUTTON_SPACING, BUTTON_WIDTH - 40, 40),
        ("Timer R", 20, BUTTON_Y_START + 2 * BUTTON_SPACING, BUTTON_WIDTH - 40, 40),
        ("All Solve", 20, BUTTON_Y_START + 4 * BUTTON_SPACING, BUTTON_WIDTH - 40, 40),
        ("Generate", 20, BUTTON_Y_START + 6 * BUTTON_SPACING, BUTTON_WIDTH - 40, 40)
    ]
    mouse_pos = pygame.mouse.get_pos()
    for text, x, y, w, h in buttons:
        is_hover = x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h
        pygame.draw.rect(screen, NEUMORPHIC_LIGHT, (x + 5, y + 5, w, h), border_radius=15)
        pygame.draw.rect(screen, NEUMORPHIC_DARK, (x - 5, y - 5, w, h), border_radius=15)
        color = TEAL if not is_hover else GLOW_TEAL
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=15)
        button_text = font.render(text, True, WHITE)
        text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(button_text, text_rect)

def check_solution():
    global invalid_cell
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                temp = grid[i][j]
                grid[i][j] = 0
                if not is_valid(i, j, temp):
                    grid[i][j] = temp
                    invalid_cell = (i, j)
                    return False, (i, j)
                grid[i][j] = temp
    invalid_cell = None
    return True, None

def is_valid(row, col, num):
    for x in range(9):
        if x != col and grid[row][x] == num:
            return False
    for x in range(9):
        if x != row and grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if (start_row + i != row or start_col + j != col) and grid[start_row + i][start_col + j] == num:
                return False
    return True

def fade_in_cell(row, col, value):
    alpha = 0
    while alpha < 255:
        screen.fill(DARK_GRAY)
        draw_background()
        draw_title()
        draw_grid()
        draw_buttons()
        draw_hints_and_status()
        if selected_cell:
            r, c = selected_cell
            pygame.draw.rect(screen, TEAL, (GRID_X + c * CELL_SIZE, GRID_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
        temp_surface = font.render(str(value), True, WHITE)
        temp_surface.set_alpha(alpha)
        screen.blit(temp_surface, (GRID_X + 5 + col * CELL_SIZE, GRID_Y + 5 + row * CELL_SIZE))
        pygame.display.flip()
        alpha += 25
        pygame.time.delay(20)

def draw_hints_and_status():
    hint_surface = small_font.render(hint_text, True, WHITE)
    status_surface = small_font.render(status_text, True, WHITE)
    difficulty_surface = small_font.render(difficulty_text, True, WHITE)
    pygame.draw.rect(screen, (0, 0, 0, 128), (GRID_X - 5, 465, GRID_WIDTH + 10, 110))
    pygame.draw.rect(screen, (40, 40, 60), (GRID_X, 470, GRID_WIDTH, 100), border_radius=10)
    screen.blit(hint_surface, (GRID_X + 5, 475))
    screen.blit(status_surface, (GRID_X + 5, 515))
    screen.blit(difficulty_surface, (GRID_X + 5, 555))

def main():
    global grid, selected_cell, move_count, start_time, paused, hint_text, status_text, difficulty_text, invalid_cell
    generate_puzzle_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell = get_cell_from_pos(pos)
                selected_cell = cell if cell else selected_cell
                if 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START <= pos[1] <= BUTTON_Y_START + 40:
                    paused = True
                elif 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START + BUTTON_SPACING <= pos[1] <= BUTTON_Y_START + BUTTON_SPACING + 40:
                    paused = False
                elif 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START + 2 * BUTTON_SPACING <= pos[1] <= BUTTON_Y_START + 2 * BUTTON_SPACING + 40:
                    start_time = time.time()
                elif 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START + 3 * BUTTON_SPACING <= pos[1] <= BUTTON_Y_START + 3 * BUTTON_SPACING + 40:
                    paused = True
                elif 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START + 4 * BUTTON_SPACING <= pos[1] <= BUTTON_Y_START + 4 * BUTTON_SPACING + 40:
                    solve_puzzle()
                elif 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START + 5 * BUTTON_SPACING <= pos[1] <= BUTTON_Y_START + 5 * BUTTON_SPACING + 40:
                    generate_puzzle_game()
                elif 20 <= pos[0] <= BUTTON_WIDTH - 20 and BUTTON_Y_START + 6 * BUTTON_SPACING <= pos[1] <= BUTTON_Y_START + 6 * BUTTON_SPACING + 40:
                    generate_puzzle_game()
            elif event.type == pygame.KEYDOWN and selected_cell and not paused:
                if event.unicode.isdigit() and 0 <= int(event.unicode) <= 9:
                    row, col = selected_cell
                    grid[row][col] = int(event.unicode)
                    move_count += 1

        current_time = time.time() - start_time if not paused else time.time() - start_time
        minutes, seconds = divmod(int(current_time), 60)
        status_text = f"Time: {minutes:02d}:{seconds:02d}"
        is_valid_solution, invalid_cell_data = check_solution()
        if not is_valid_solution and invalid_cell_data:
            row, col = invalid_cell_data
            hint_text = f"Hint: Invalid at row {row+1}, col {col+1}"
        else:
            hint_text = "Hint: everything is well"

        screen.fill(DARK_GRAY)
        draw_background()
        draw_title()
        draw_grid()
        draw_buttons()
        draw_hints_and_status()
        if selected_cell and not paused:
            row, col = selected_cell
            pygame.draw.rect(screen, TEAL, (GRID_X + col * CELL_SIZE, GRID_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def solve_puzzle():
    global grid, move_count
    temp_grid = [row[:] for row in grid]
    if solve(temp_grid):
        for i in range(9):
            for j in range(9):
                if temp_grid[i][j] != grid[i][j]:
                    fade_in_cell(i, j, temp_grid[i][j])
        grid = temp_grid
        move_count += 1

def generate_puzzle_game():
    global grid, move_count, start_time, hint_text, difficulty_text
    puzzle, _ = generate_puzzle(blanks=40)
    grid = puzzle
    move_count = 0
    start_time = time.time()
    hint_text = "Hint: everything is well"

    # ✅ Measure difficulty using solve time
    difficulty, _ = measure_difficulty_time(grid)
    difficulty_text = f"Difficulty: {difficulty}"

if __name__ == "__main__":
    main()
