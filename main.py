import tkinter as tk
from tkinter import messagebox

# Constants for the game
ROWS = 6
COLS = 7
EMPTY = ' '
PLAYER1 = 'X'
PLAYER2 = 'O'

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.board = self.create_board()
        self.current_player = PLAYER1
        self.buttons = []
        self.create_widgets()
        self.root.bind("<Configure>", self.on_resize)

    def create_board(self):
        return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def create_widgets(self):
        # Create a frame for the buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons for each column
        for col in range(COLS):
            button = tk.Button(self.frame, text=str(col), command=lambda c=col: self.handle_click(c))
            button.grid(row=0, column=col, sticky=tk.NSEW)
            self.buttons.append(button)

        # Create labels for the board cells
        self.labels = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                label = tk.Label(self.frame, text=EMPTY, width=2, height=1, borderwidth=2, relief="groove", font=("Helvetica", 24))
                label.grid(row=row+1, column=col, sticky=tk.NSEW)
                self.labels[row][col] = label

        # Set grid weights to make widgets resize with window
        for col in range(COLS):
            self.frame.grid_columnconfigure(col, weight=1)
        for row in range(ROWS+1):  # +1 for the row of buttons
            self.frame.grid_rowconfigure(row, weight=1)

    def handle_click(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.current_player)
            self.update_board()

            if self.winning_move(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(COLS-3):
            for r in range(ROWS):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return True
        # Check vertical locations for win
        for c in range(COLS):
            for r in range(ROWS-3):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return True
        # Check positively sloped diagonals
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return True
        # Check negatively sloped diagonals
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if all(self.board[r-i][c+i] == piece for i in range(4)):
                    return True
        return False

    def is_board_full(self):
        return all(self.board[0][col] != EMPTY for col in range(COLS))

    def update_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.labels[row][col].config(text=self.board[row][col])

    def reset_game(self):
        self.board = self.create_board()
        self.update_board()
        self.current_player = PLAYER1

    def on_resize(self, event):
        max_cell_size = 50  # Set a maximum size for each cell
        min_cell_size = 20  # Set a minimum size for each cell

        new_width = min(self.frame.winfo_width() // COLS, max_cell_size)
        new_height = min((self.frame.winfo_height() // (ROWS + 1)), max_cell_size)
        
        new_width = max(new_width, min_cell_size)
        new_height = max(new_height, min_cell_size)

        for row in range(ROWS):
            for col in range(COLS):
                font_size = min(new_width // 2, 24)
                self.labels[row][col].config(width=new_width//10, height=new_height//20, font=("Helvetica", font_size))

        for button in self.buttons:
            button.config(width=new_width//10, height=new_height//40, font=("Helvetica", min(new_width//3, 12)))

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()
