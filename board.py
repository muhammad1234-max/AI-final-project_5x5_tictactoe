class Board:
    def __init__(self):
        self.size = 5
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.empty_cells = [(i, j) for i in range(self.size) for j in range(self.size)]
    
    def make_move(self, row, col, player):
        """
        Make a move on the board
        player: 1 for human (X), 2 for AI (O)
        Returns True if move is valid, False otherwise
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
            self.board[row][col] = player
            self.empty_cells.remove((row, col))
            return True
        return False
    
    def undo_move(self, row, col):
        """
        Undo a move (used by AI algorithm)
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] != 0:
            self.board[row][col] = 0
            self.empty_cells.append((row, col))
    
    def is_cell_empty(self, row, col):
        """
        Check if a cell is empty
        """
        return self.board[row][col] == 0
    
    def get_empty_cells(self):
        """
        Return a list of empty cells
        """
        return self.empty_cells
    
    def is_board_full(self):
        """
        Check if the board is full
        """
        return len(self.empty_cells) == 0
    
    def get_cell_state(self, row, col):
        """
        Get the state of a cell
        Returns 0 for empty, 1 for human (X), 2 for AI (O)
        """
        return self.board[row][col]
    
    def reset(self):
        """
        Reset the board to initial state
        """
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.empty_cells = [(i, j) for i in range(self.size) for j in range(self.size)]