import tkinter as tk
from tkinter import messagebox
import random

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
        self.move_history = []
        self.rounds = 1
        self.score = {PLAYER1: 0, PLAYER2: 0}
        self.buttons = []
        self.ai_mode = False
        self.create_widgets()
        self.create_menu()
        self.root.bind("<Configure>", self.on_resize)
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
        self.frame = tk.Frame(self.root, bg="lightblue")
        self.frame.pack(fill=tk.BOTH, expand=True)

        for col in range(COLS):
            button = tk.Button(self.frame, text=str(col + 1), command=lambda c=col: self.handle_click(c), bg="navy", fg="white", font=("Helvetica", 16, "bold"))
            button.grid(row=0, column=col, sticky=tk.NSEW)
            button.bind("<Enter>", lambda event, b=button: b.config(bg="royalblue"))
            button.bind("<Leave>", lambda event, b=button: b.config(bg="navy"))
            self.buttons.append(button)

        self.labels = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                label = tk.Label(self.frame, text=EMPTY, width=2, height=1, borderwidth=2, relief="groove", font=("Helvetica", 24), bg="white")
                label.grid(row=row+1, column=col, sticky=tk.NSEW)
                self.labels[row][col] = label

        self.round_label = tk.Label(self.frame, text=f"Round: {self.rounds} | {PLAYER1}: {self.score[PLAYER1]} | {PLAYER2}: {self.score[PLAYER2]}", bg="lightblue", font=("Helvetica", 16, "bold"))
        self.round_label.grid(row=ROWS+1, column=0, columnspan=COLS, sticky=tk.NSEW)

        for col in range(COLS):
            self.frame.grid_columnconfigure(col, weight=1)
        for row in range(ROWS+2):
            self.frame.grid_rowconfigure(row, weight=1)

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.mode_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Mode", menu=self.mode_menu)
        self.mode_menu.add_command(label="2 Player Mode", command=self.start_two_player_mode)
        self.mode_menu.add_command(label="Play Against AI", command=self.start_ai_mode)
        self.menubar.add_command(label="Undo", command=self.undo_move)

    def start_two_player_mode(self):
        self.ai_mode = False
        self.reset_game()
        self.update_mode_label()

    def start_ai_mode(self):
        self.ai_mode = True
        self.reset_game()
        self.update_mode_label()

    def update_mode_label(self):
        mode = "AI Mode" if self.ai_mode else "2 Player Mode"
        self.round_label.config(text=f"Mode: {mode} | Round: {self.rounds} | {PLAYER1}: {self.score[PLAYER1]} | {PLAYER2}: {self.score[PLAYER2]}")

    def handle_click(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.current_player)
            self.move_history.append((row, col, self.current_player))
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
                if self.ai_mode and self.current_player == PLAYER2:
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        col = self.find_best_move()
        if col is not None:
            self.handle_click(col)

    def find_best_move(self):
        for col in range(COLS):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, PLAYER2)
                if self.winning_move(PLAYER2):
                    self.board[row][col] = EMPTY
                    return col
                self.board[row][col] = EMPTY
        for col in range(COLS):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, PLAYER1)
                if self.winning_move(PLAYER1):
                    self.board[row][col] = EMPTY
                    return col
                self.board[row][col] = EMPTY
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
        for c in range(COLS-3):
            for r in range(ROWS):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return True
        for c in range(COLS):
            for r in range(ROWS-3):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return True
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return True
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
        self.move_history.clear()
        self.update_board()
        self.current_player = PLAYER1

    def next_round(self):
        self.rounds += 1
        self.reset_game()
        self.update_mode_label()

    def undo_move(self):
        if self.move_history:
            row, col, player = self.move_history.pop()
            self.board[row][col] = EMPTY
            self.update_board()
            self.current_player = player

    def on_resize(self, event):
        max_cell_size = 50
        min_cell_size = 20
        new_width = min(self.frame.winfo_width() // COLS, max_cell_size)
        new_height = min((self.frame.winfo_height() // (ROWS + 2)), max_cell_size)
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
