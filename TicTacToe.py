import pygame
import sys
import random
import tkinter as tk
from tkinter import simpledialog

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Fonts
font = pygame.font.Font(None, 60)

def initialize_board(grid_size):
    return [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

def draw_board(grid_size):
    screen.fill(WHITE)
    for i in range(1, grid_size):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE[1]), 3)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE[0], i * CELL_SIZE), 3)

def draw_symbols(board):
    for row in range(len(board)):
        for col in range(len(board)):
            symbol = board[row][col]
            if symbol == 'X':
                draw_X(row, col)
            elif symbol == 'O':
                draw_O(row, col)

def draw_X(row, col):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    offset = CELL_SIZE // 4
    pygame.draw.line(screen, RED, (x - offset, y - offset), (x + offset, y + offset), 5)
    pygame.draw.line(screen, RED, (x + offset, y - offset), (x - offset, y + offset), 5)

def draw_O(row, col):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 4
    pygame.draw.circle(screen, RED, (x, y), radius, 3)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

def is_board_full(board):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == ' ':
                return False
    return True

def is_winner(board, symbol):
    # Check rows and columns
    for i in range(len(board)):
        if all(board[i][j] == symbol for j in range(len(board))) or \
           all(board[j][i] == symbol for j in range(len(board))):
            return True

    # Check diagonals
    if all(board[i][i] == symbol for i in range(len(board))) or \
       all(board[i][len(board) - 1 - i] == symbol for i in range(len(board))):
        return True

    return False

def get_empty_cells(board):
    empty_cells = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == ' ':
                empty_cells.append((row, col))
    return empty_cells

def evaluate(board, symbol):
    # Check rows, columns, and diagonals for winning combinations
    for i in range(len(board)):
        if all(board[i][j] == symbol for j in range(len(board))):
            return True
        if all(board[j][i] == symbol for j in range(len(board))):
            return True
    if all(board[i][i] == symbol for i in range(len(board))) or \
       all(board[i][len(board) - 1 - i] == symbol for i in range(len(board))):
        return True
    return False

def minimax(board, depth, is_maximizing, alpha, beta):
    if evaluate(board, 'O'):
        return 10 - depth
    elif evaluate(board, 'X'):
        return depth - 10
    elif is_board_full(board):
        return 0

    if depth == 3:
        return 0

    if is_maximizing:
        max_eval = -1000
        empty_cells = get_empty_cells(board)
        for cell in empty_cells:
            row, col = cell
            board[row][col] = 'O'
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[row][col] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 1000
        empty_cells = get_empty_cells(board)
        for cell in empty_cells:
            row, col = cell
            board[row][col] = 'X'
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[row][col] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board):
    best_eval = -1000
    best_move = (-1, -1)
    empty_cells = get_empty_cells(board)
    for cell in empty_cells:
        row, col = cell
        board[row][col] = 'O'
        eval = minimax(board, 0, False, -1000, 1000)
        board[row][col] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = (row, col)
    return best_move

def start_game():
    global grid_size, mode, difficulty
    grid_size = int(entry.get())
    mode = mode_var.get()
    if mode == 'AI':
        difficulty = difficulty_var.get()
    root.destroy()

def get_user_input():
    global root, entry, mode_var, difficulty_var
    root = tk.Tk()
    root.title("Tic Tac Toe Settings")
    label = tk.Label(root, text="Enter the size of the grid (3 to 5):")
    label.pack()
    entry = tk.Entry(root)
    entry.pack()
    mode_var = tk.StringVar(root)
    mode_var.set("Multiplayer")
    mode_menu = tk.OptionMenu(root, mode_var, "Multiplayer", "AI")
    mode_menu.pack()
    difficulty_var = tk.StringVar(root)
    difficulty_var.set("Easy")
    difficulty_menu = tk.OptionMenu(root, difficulty_var, "Easy", "Medium", "Hard")
    difficulty_menu.pack()
    button = tk.Button(root, text="Start Game", command=start_game)
    button.pack()
    root.mainloop()

def display_message(message):
    tk.messagebox.showinfo("Game Result", message)

def main():
    get_user_input()
    global grid_size, mode, difficulty
    if grid_size < 3 or grid_size > 5:
        print("Invalid grid size. Please choose between 3 and 5.")
        return

    # Set up the screen
    global CELL_SIZE, WINDOW_SIZE, screen
    CELL_SIZE = 100
    WINDOW_SIZE = (grid_size * CELL_SIZE, grid_size * CELL_SIZE)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Tic Tac Toe")

    board = initialize_board(grid_size)
    current_symbol = 'X'
    game_result = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_result is None:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if board[row][col] == ' ':
                    board[row][col] = current_symbol
                    if is_winner(board, current_symbol):
                        game_result = f"Player {current_symbol} wins!"
                    elif is_board_full(board):
                        game_result = "It's a draw!"
                    else:
                        current_symbol = 'O' if current_symbol == 'X' else 'X'

                    # AI Move
                    if mode == 'AI' and current_symbol == 'O' and game_result is None:
                        if difficulty == 'Easy':
                            row, col = random.choice(get_empty_cells(board))
                        elif difficulty == 'Medium' or difficulty == 'Hard':
                            row, col = find_best_move(board)
                        board[row][col] = current_symbol
                        if is_winner(board, current_symbol):
                            game_result = f"Player {current_symbol} wins!"
                        elif is_board_full(board):
                            game_result = "It's a draw!"
                        else:
                            current_symbol = 'X'

        draw_board(grid_size)
        draw_symbols(board)
        pygame.display.flip()

        if game_result:
            display_message(game_result)
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()

