def create_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 13)
    print('0 1 2 3 4 5 6')

def is_valid_location(board, col):
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(5, -1, -1):
        if board[r][col] == ' ':
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(4):
        for r in range(6):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical locations for win
    for c in range(7):
        for r in range(3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check positively sloped diagonals
    for c in range(4):
        for r in range(3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for c in range(4):
        for r in range(3, 6):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def switch_player(current_player):
    return 'O' if current_player == 'X' else 'X'

def play_game():
    board = create_board()
    game_over = False
    current_player = 'X'

    while not game_over:
        print_board(board)
        col = int(input(f"Player {current_player}, make your selection (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, current_player)

            if winning_move(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                game_over = True
            else:
                current_player = switch_player(current_player)
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    play_game()
def play_game():
    board = create_board()
    game_over = False
    current_player = 'X'

    while not game_over:
        print_board(board)
        try:
            col = int(input(f"Player {current_player}, make your selection (0-6): "))
            if col < 0 or col > 6:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 6.")
            continue

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, current_player)

            if winning_move(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                game_over = True
            else:
                current_player = switch_player(current_player)
        else:
            print("Invalid selection. Column is full. Try again.")

if __name__ == "__main__":
    play_game()
