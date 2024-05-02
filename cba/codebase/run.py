from tictactoe import *

def play_game():
    while True:
        display_board()
        position = int(input(f"Player {current_player}, choose a position (1-9): ")) - 1

        if position not in range(9):
            print("Invalid position. Please choose a position between 1 and 9.")
            continue

        if place_mark(position):
            if check_win(current_player):
                display_board()
                print(f"Player {current_player} wins!")
                break
            if check_draw():
                display_board()
                print("It's a draw!")
                break
            switch_player()
        else:
            print("That position is already taken. Please choose another position.")

if __name__ == "__main__":
    play_game()
