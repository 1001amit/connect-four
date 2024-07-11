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

