import tkinter as tk
from tkinter import messagebox
import random

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
        self.move_history = []  # To track the moves made for undo functionality
        self.rounds = 1
        self.score = {PLAYER1: 0, PLAYER2: 0}
        self.buttons = []
        self.create_widgets()
        self.root.bind("<Configure>", self.on_resize)

        # Bind keyboard keys for column selection
        self.root.bind("1", lambda event: self.handle_click(0))
        self.root.bind("2", lambda event: self.handle_click(1))
        self.root.bind("3", lambda event: self.handle_click(2))
        self.root.bind("4", lambda event: self.handle_click(3))
        self.root.bind("5", lambda event: self.handle_click(4))
        self.root.bind("6", lambda event: self.handle_click(5))
        self.root.bind("7", lambda event: self.handle_click(6))

    def create_board(self):
        return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    def create_widgets(self):
        # Create a frame for the buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons for each column with hover effects
        for col in range(COLS):
            button = tk.Button(self.frame, text=str(col + 1), command=lambda c=col: self.handle_click(c))
            button.grid(row=0, column=col, sticky=tk.NSEW)
            button.bind("<Enter>", lambda event, b=button: b.config(bg="lightblue"))  # Change background on hover
            button.bind("<Leave>", lambda event, b=button: b.config(bg="SystemButtonFace"))  # Restore background on leave
            self.buttons.append(button)

        # Create an undo button with hover effect
        undo_button = tk.Button(self.frame, text="Undo", command=self.undo_move)
        undo_button.grid(row=0, column=COLS, sticky=tk.NSEW)
        undo_button.bind("<Enter>", lambda event, b=undo_button: b.config(bg="lightgreen"))  # Change background on hover
        undo_button.bind("<Leave>", lambda event, b=undo_button: b.config(bg="SystemButtonFace"))  # Restore background on leave

        # Create a label to display the round number and score
        self.round_label = tk.Label(self.frame, text=f"Round: {self.rounds} | {PLAYER1}: {self.score[PLAYER1]} | {PLAYER2}: {self.score[PLAYER2]}")
        self.round_label.grid(row=0, column=COLS+1, sticky=tk.NSEW)

        # Create labels for the board cells
        self.labels = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                label = tk.Label(self.frame, text=EMPTY, width=2, height=1, borderwidth=2, relief="groove", font=("Helvetica", 24))
                label.grid(row=row+1, column=col, sticky=tk.NSEW)
                self.labels[row][col] = label

        # Set grid weights to make widgets resize with window
        for col in range(COLS + 2):  # +2 for the undo button and round label
            self.frame.grid_columnconfigure(col, weight=1)
        for row in range(ROWS + 1):  # +1 for the row of buttons
            self.frame.grid_rowconfigure(row, weight=1)

    def handle_click(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.current_player)
            self.move_history.append((row, col, self.current_player))  # Track the move
            self.update_board()

            if self.winning_move(self.current_player):
                self.score[self.current_player] += 1
                messagebox.showinfo("Round Over", f"Player {self.current_player} wins round {self.rounds}!")
                self.next_round()
            elif self.is_board_full():
                messagebox.showinfo("Round Over", f"It's a tie in round {self.rounds}!")
                self.next_round()
            else:
                self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
                if self.current_player == PLAYER2:
                    self.root.after(500, self.ai_move)  # AI makes a move after 500ms delay

    def ai_move(self):
        col = self.find_best_move()
        if col is not None:
            self.handle_click(col)

    def find_best_move(self):
        # Check if AI can win in the next move
        for col in range(COLS):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, PLAYER2)
                if self.winning_move(PLAYER2):
                    self.board[row][col] = EMPTY
                    return col
                self.board[row][col] = EMPTY

        # Check if player can win in the next move and block them
        for col in range(COLS):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, PLAYER1)
                if self.winning_move(PLAYER1):
                    self.board[row][col] = EMPTY
                    return col
                self.board[row][col] = EMPTY

        # Choose a random valid column
        valid_columns = [col for col in range(COLS) if self.is_valid_location(col)]
        return random.choice(valid_columns) if valid_columns else None

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
        self.move_history.clear()  # Clear the move history
        self.update_board()
        self.current_player = PLAYER1

    def next_round(self):
        self.rounds += 1
        self.reset_game()
        self.round_label.config(text=f"Round: {self.rounds} | {PLAYER1}: {self.score[PLAYER1]} | {PLAYER2}: {self.score[PLAYER2]}")

    def undo_move(self):
        if self.move_history:
            row, col, _ = self.move_history.pop()  # Get the last move
            self.board[row][col] = EMPTY  # Remove the piece from the board
            self.update_board()
            self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1  # Switch back to the previous player

    def on_resize(self, event):
        max_cell_size = 50  # Set a maximum size for each cell
        min_cell_size = 20  # Set a minimum size for each cell

        new_width = min(self.frame.winfo_width() // (COLS + 2), max_cell_size)  # +2 for the undo button and round label
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
