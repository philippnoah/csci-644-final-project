# Tic Tac Toe Game Logic

# Global Variables
board = [' ' for _ in range(9)]
current_player = 'X'

# Function to display the board
def display_board():
    for i in range(0, 9, 3):
        print(f'{board[i]} | {board[i + 1]} | {board[i + 2]}')
        if i < 6:
            print('-' * 5)

# Function to check if a player has won
def check_win(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if all(board[pos] == player for pos in condition):
            return True
    return False

# Function to check for a draw
def check_draw():
    return ' ' not in board

# Function to switch player turns
def switch_player():
    global current_player
    current_player = 'O' if current_player == 'X' else 'X'

# Function to place a player's mark on the board
def place_mark(position):
    if board[position] == ' ':
        board[position] = current_player
        return True
    return False
