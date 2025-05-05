import tkinter as tk
from tkinter import messagebox
import time
import random
from tkinter import font as tkfont
import math

class GUI:
    def __init__(self, root, board, game_logic, ai):
        self.root = root
        self.board = board
        self.game_logic = game_logic
        self.ai = ai
        
     
        # Modern dark theme color palette
        self.bg_color = '#0f0f1a'  # Deep blue-black background
        self.header_color = '#1a1a2e'  # Slightly lighter than background
        self.btn_color = '#16213e'  # Dark blue for buttons
        self.btn_hover_color = '#1e2a4a'  # Lighter blue for hover
        self.human_color = '#00cec9'  # Teal for human player
        self.ai_color = '#fd79a8'  # Pink for AI player
        self.win_line_color = '#6c5ce7'  # Purple for win highlight
        self.text_color = '#ffffff'  # White text
        self.accent_color = '#6c5ce7'  # Vibrant purple accent
        
       
        self.player_score = 0
        self.ai_score = 0
        self.winning_cells = []
        
        
        self.root.configure(bg=self.bg_color)
        self.root.resizable(True, True)
        self.root.title("Modern Tic Tac Toe")
        
        
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=14)
        self.button_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        
        # Create frames
        self.header_frame = tk.Frame(root, bg=self.header_color, padx=20, pady=15)
        self.header_frame.pack(fill=tk.X, pady=0)
        
        self.score_frame = tk.Frame(root, bg=self.bg_color, padx=20, pady=10)
        self.score_frame.pack(fill=tk.X)
        
        self.board_frame = tk.Frame(root, bg=self.bg_color, padx=20, pady=15)
        self.board_frame.pack(pady=10)
        
        self.footer_frame = tk.Frame(root, bg=self.bg_color, padx=20, pady=15)
        self.footer_frame.pack(pady=10, fill=tk.X)
        
        
        self.title_label = tk.Label(self.header_frame, text="5×5 Tic Tac Toe", 
                                  font=self.title_font, bg=self.header_color, fg=self.text_color)
        self.title_label.pack(pady=10)
        
        
        self.score_frame_left = tk.Frame(self.score_frame, bg=self.bg_color)
        self.score_frame_left.pack(side=tk.LEFT, expand=True)
        
        self.score_frame_right = tk.Frame(self.score_frame, bg=self.bg_color)
        self.score_frame_right.pack(side=tk.RIGHT, expand=True)
        
        self.player_score_label = tk.Label(self.score_frame_left, text="YOU: 0", 
                                         font=self.status_font, bg=self.bg_color, fg=self.human_color)
        self.player_score_label.pack(side=tk.LEFT, padx=15)
        
        self.ai_score_label = tk.Label(self.score_frame_right, text="AI: 0", 
                                     font=self.status_font, bg=self.bg_color, fg=self.ai_color)
        self.ai_score_label.pack(side=tk.RIGHT, padx=15)
        
        
        self.status_frame = tk.Frame(self.score_frame, bg=self.bg_color)
        self.status_frame.pack(pady=10)
        
        self.status_label = tk.Label(self.status_frame, text="YOUR TURN", 
                                    font=self.status_font, bg=self.bg_color, fg=self.text_color,
                                    padx=15, pady=5)
        self.status_label.pack()
        
        
        self.pulse_direction = 1
        self.pulse_intensity = 0
        self.pulse_status_label()
        
        
        self.buttons = []
        for row in range(board.size):
            button_row = []
            for col in range(board.size):
                button = tk.Button(self.board_frame, text="", width=3, height=1, 
                                  font=self.button_font, bg=self.btn_color, fg=self.text_color,
                                  activebackground=self.btn_hover_color, activeforeground=self.text_color,
                                  bd=0, relief=tk.FLAT, cursor="hand2",
                                  command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row, column=col, padx=4, pady=4, ipadx=8, ipady=8)
                
               
                button.bind("<Enter>", lambda event, btn=button: self.on_button_hover(btn))
                button.bind("<Leave>", lambda event, btn=button: self.on_button_leave(btn))
                
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Create footer with buttons
        self.button_frame = tk.Frame(self.footer_frame, bg=self.bg_color)
        self.button_frame.pack()
        
        
        self.reset_button = tk.Button(self.button_frame, text="NEW GAME", font=self.status_font,
                                     command=self.reset_game, bg=self.human_color, fg=self.text_color,
                                     activebackground="#0097a7", activeforeground=self.text_color,
                                     relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.reset_button.pack(side=tk.LEFT, padx=15)
        
        
        self.difficulty_level = 3  
        self.difficulty_button = tk.Button(self.button_frame, text="DIFFICULTY: MEDIUM", 
                                         font=self.status_font, command=self.change_difficulty,
                                         bg=self.accent_color, fg=self.text_color, 
                                         activebackground="#5e35b1", activeforeground=self.text_color,
                                         relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.difficulty_button.pack(side=tk.LEFT, padx=15)
    
    def pulse_status_label(self):
        """Create a pulsing effect for the status label"""
        
        self.pulse_intensity += 0.05 * self.pulse_direction
        if self.pulse_intensity >= 1.0:
            self.pulse_direction = -1
        elif self.pulse_intensity <= 0.0:
            self.pulse_direction = 1
            
        
        base_color = self.human_color if self.game_logic.get_current_player() == 1 else self.ai_color
        
    
        if not self.game_logic.is_game_over():
            self.status_label.config(fg=base_color)
        
        self.root.after(50, self.pulse_status_label)
    
    def on_button_hover(self, button):
        """Add hover effect to buttons"""
        if button["state"] != tk.DISABLED:
            button.config(bg=self.btn_hover_color)
           
            current_player = self.game_logic.get_current_player()
            glow_color = self.human_color if current_player == 1 else self.ai_color
            button.config(highlightbackground=glow_color, highlightthickness=2)
    
    def on_button_leave(self, button):
        """Remove hover effect from buttons"""
        if button["state"] != tk.DISABLED:
            button.config(bg=self.btn_color, highlightthickness=0)
    
    def change_difficulty(self):
        """Change AI difficulty level with visual feedback"""
        levels = [(1, "EASY", "#4caf50"), (3, "MEDIUM", "#ff9800"), (5, "HARD", "#f44336")]
        current_index = next((i for i, (level, _, _) in enumerate(levels) if level == self.difficulty_level), 0)
        next_index = (current_index + 1) % len(levels)
        self.difficulty_level, difficulty_name, color = levels[next_index]
        
        self.ai.max_depth = self.difficulty_level
        self.ai.difficulty = difficulty_name.lower()
        
        original_bg = self.difficulty_button["bg"]
        self.difficulty_button.config(bg=color)
        self.root.after(200, lambda: self.difficulty_button.config(bg=self.accent_color))
        
        self.difficulty_button.config(text=f"DIFFICULTY: {difficulty_name}")
    
    def highlight_winning_cells(self):
        """Highlight the winning cells with animation"""
        if not self.winning_cells:
            return
            
        def animate_cell(index):
            if index < len(self.winning_cells):
                row, col = self.winning_cells[index]
                button = self.buttons[row][col]
                
                # Flash effect
                for i in range(3):
                    button.config(bg=self.win_line_color)
                    self.root.update()
                    time.sleep(0.05)
                    button.config(bg=self.btn_color)
                    self.root.update()
                    time.sleep(0.05)
                
               
                button.config(bg=self.win_line_color)
                
                
                self.root.after(100, lambda: animate_cell(index + 1))
        
        
        animate_cell(0)
    
    def handle_button_click(self, row, col):
        """
        Handle button click event
        """
        if self.game_logic.is_game_over() or self.game_logic.get_current_player() != 1:
            return
        
        if self.game_logic.make_move(row, col):
          
            self.animate_move(row, col, "X", self.human_color)
            
            if self.game_logic.is_game_over():
                self.find_winning_cells()
                self.highlight_winning_cells()
                self.show_game_result()
                return
            
        
            self.animate_thinking()
            self.root.update() 
            
            self.root.after(random.randint(300, 800))
            
            self.make_ai_move()
    
    def animate_thinking(self):
        """Animate the AI thinking status with dots"""
        dots = [".  ", ".. ", "..."]
        for i in range(3):
            self.status_label.config(text=f"AI IS THINKING{dots[i]}", fg=self.ai_color)
            self.root.update()
            time.sleep(0.2)
    
    def animate_move(self, row, col, symbol, color):
        """Animate a move with enhanced visual effects"""
        button = self.buttons[row][col]
        button.config(text="", state=tk.DISABLED)
        
       
        for i in range(5):
            size = i * 0.2
            alpha = 1.0 - (i * 0.2)
            button.config(bg=color)
            self.root.update()
            time.sleep(0.05)
            button.config(bg=self.btn_color)
            self.root.update()
            time.sleep(0.02)
        
        for opacity in range(0, 11, 2):
           
            opacity_factor = opacity / 10.0
            button.config(text=symbol, disabledforeground=color, bg=self.btn_color)
            self.root.update()
            time.sleep(0.03)
        
        
        button.config(text=symbol, disabledforeground=color, bg=self.btn_color)
    
    def find_winning_cells(self):
        """Find the cells that form the winning line"""
        self.winning_cells = []
        winner = self.game_logic.get_winner()
        if winner is None:  
            return
            
        board_size = self.board.size
        board_state = self.board.board
        
        
        for row in range(board_size):
            for col in range(board_size - 4):
                if all(board_state[row][col+i] == winner for i in range(5)):
                    self.winning_cells = [(row, col+i) for i in range(5)]
                    return
        
       
        for row in range(board_size - 4):
            for col in range(board_size):
                if all(board_state[row+i][col] == winner for i in range(5)):
                    self.winning_cells = [(row+i, col) for i in range(5)]
                    return
        
    
        for row in range(board_size - 4):
            for col in range(board_size - 4):
                if all(board_state[row+i][col+i] == winner for i in range(5)):
                    self.winning_cells = [(row+i, col+i) for i in range(5)]
                    return
        
       
        for row in range(4, board_size):
            for col in range(board_size - 4):
                if all(board_state[row-i][col+i] == winner for i in range(5)):
                    self.winning_cells = [(row-i, col+i) for i in range(5)]
                    return
    
    def make_ai_move(self):
        """
        Make a move for the AI
        """
  
        ai_row, ai_col = self.ai.make_move(self.board, self.game_logic)
        
      
        if self.game_logic.make_move(ai_row, ai_col):
          
            self.animate_move(ai_row, ai_col, "O", self.ai_color)
            
          
            if self.game_logic.is_game_over():
                self.find_winning_cells()
                self.highlight_winning_cells()
                self.show_game_result()
            else:
                self.status_label.config(text="YOUR TURN", fg=self.human_color)
    
    def show_game_result(self):
        """
        Show the game result with enhanced visuals
        """
        winner = self.game_logic.get_winner()
        
        
        result_window = tk.Toplevel(self.root)
        result_window.configure(bg=self.bg_color)
        result_window.title("Game Result")
        result_window.geometry("300x200")
        result_window.resizable(False, False)
        result_window.transient(self.root) 
        result_window.grab_set()  
        
        result_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                         self.root.winfo_rooty() + 50))
        
        content_frame = tk.Frame(result_window, bg=self.bg_color, padx=20, pady=20)
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        if winner == 1:
            self.player_score += 1
            self.player_score_label.config(text=f"You: {self.player_score}")
            self.status_label.config(text="YOU WIN! 🎉", fg=self.human_color)
            
            result_text = "Congratulations!\nYou Win! 🎉"
            result_color = self.human_color
            
        elif winner == 2:
            self.ai_score += 1
            self.ai_score_label.config(text=f"AI: {self.ai_score}")
            self.status_label.config(text="AI WINS! 🤖", fg=self.ai_color)
            
            result_text = "AI Wins!\nBetter luck next time 🤖"
            result_color = self.ai_color
            
        else:
            self.status_label.config(text="IT'S A DRAW! 🤝", fg=self.text_color)
            
            result_text = "It's a Draw!\nWell played 🤝"
            result_color = self.text_color
        
        
        result_label = tk.Label(content_frame, text=result_text, font=("Arial", 18, "bold"),
                              bg=self.bg_color, fg=result_color, justify=tk.CENTER)
        result_label.pack(pady=10)
        
        score_text = f"Score: You {self.player_score} - {self.ai_score} AI"
        score_label = tk.Label(content_frame, text=score_text, font=("Arial", 12),
                             bg=self.bg_color, fg=self.text_color)
        score_label.pack(pady=5)
        
        # Close button
        close_button = tk.Button(content_frame, text="Continue", font=("Arial", 12),
                               command=result_window.destroy, bg="#3182ce", fg=self.text_color,
                               activebackground="#2b6cb0", activeforeground=self.text_color,
                               relief=tk.FLAT, padx=15, pady=5, cursor="hand2")
        close_button.pack(pady=10)
    
    def reset_game(self):
        """
        Reset the game
        """
        
        self.game_logic.reset()
        self.winning_cells = []
        
        for row in range(self.board.size):
            for col in range(self.board.size):
                self.buttons[row][col].config(text="", state=tk.NORMAL, bg=self.btn_color)
                self.root.update()
                time.sleep(0.01)  
      
        self.status_label.config(text="YOUR TURN", fg=self.human_color)
        
      
        if random.random() < 0.2:  
            self.status_label.config(text="AI GOES FIRST", fg=self.ai_color)
            self.root.update()
            
            for i in range(3, 0, -1):
                self.status_label.config(text=f"AI STARTS IN {i}")
                self.root.update()
                time.sleep(0.7)
                
            self.status_label.config(text="AI IS THINKING...", fg=self.ai_color)
            self.root.update()
            time.sleep(0.5)
            self.make_ai_move()
