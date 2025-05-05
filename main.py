import tkinter as tk
from board import Board
from game_logic import GameLogic
from ai import AI
from gui import GUI
from loading_screen import LoadingScreen
from difficulty_screen import DifficultyScreen

def main():
    # Initialize the main window
    root = tk.Tk()
    root.title("Modern Tic Tac Toe AI")
    
    # Create game components
    board = Board()
    ai = AI()
    game_logic = GameLogic(board)
    
    # Function to start the game after difficulty selection
    def start_game(difficulty, depth):
        # Update AI difficulty
        ai.difficulty = difficulty
        ai.max_depth = depth
        
        # Start the game with the selected difficulty
        gui = GUI(root, board, game_logic, ai)
    
    # Function to show difficulty screen after loading
    def show_difficulty_screen():
        difficulty_screen = DifficultyScreen(root, start_game)
    
    # Start with loading screen
    loading_screen = LoadingScreen(root, show_difficulty_screen)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()