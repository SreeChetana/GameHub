import streamlit as st
import numpy as np
import time
import random

def render_tic_tac_toe():
    st.title("Tic Tac Toe with AI")
    
    # Initialize the board if it doesn't exist
    if 'ttt_board' not in st.session_state:
        st.session_state.ttt_board = np.array([[' ' for _ in range(3)] for _ in range(3)])
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.human_turn = True
        st.session_state.difficulty = "Medium"
    
    # Game settings section
    with st.expander("Game Settings", expanded=False):
        # Difficulty levels
        difficulty = st.radio(
            "Select AI difficulty",
            ["Easy", "Medium", "Hard"],
            index=["Easy", "Medium", "Hard"].index(st.session_state.difficulty)
        )
        
        if difficulty != st.session_state.difficulty:
            st.session_state.difficulty = difficulty
        
        # Reset game button
        if st.button("Start New Game"):
            st.session_state.ttt_board = np.array([[' ' for _ in range(3)] for _ in range(3)])
            st.session_state.game_over = False
            st.session_state.winner = None
            st.session_state.human_turn = True
    
    # Display game status
    if st.session_state.game_over:
        if st.session_state.winner == 'X':
            st.success("You won! Congratulations!")
        elif st.session_state.winner == 'O':
            st.error("AI won! Better luck next time.")
        else:
            st.info("It's a draw!")
    else:
        if st.session_state.human_turn:
            st.info("Your turn (X)")
        else:
            st.info("AI's turn (O)")
    
    # Create a 3x3 grid of buttons for the tic tac toe game
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            with cols[j]:
                # Get the current cell value
                cell_value = st.session_state.ttt_board[i, j]
                
                # Create a button for each cell
                if cell_value == ' ' and not st.session_state.game_over and st.session_state.human_turn:
                    if st.button(f"   ", key=f"ttt_{i}_{j}", use_container_width=True):
                        # Human makes a move
                        st.session_state.ttt_board[i, j] = 'X'
                        st.session_state.human_turn = False
                        
                        # Check if the game is over after human's move
                        if check_winner(st.session_state.ttt_board, 'X'):
                            st.session_state.game_over = True
                            st.session_state.winner = 'X'
                        elif is_full(st.session_state.ttt_board):
                            st.session_state.game_over = True
                            st.session_state.winner = None
                        
                        # Rerun to update the UI
                        st.rerun()
                else:
                    # Display X, O or empty
                    button_label = "X" if cell_value == 'X' else "O" if cell_value == 'O' else " "
                    st.button(button_label, key=f"ttt_{i}_{j}", disabled=True, use_container_width=True)
    
    # AI's turn
    if not st.session_state.human_turn and not st.session_state.game_over:
        # Add a small delay to make it seem like the AI is thinking
        time.sleep(0.5)
        
        # AI makes a move based on the difficulty
        if st.session_state.difficulty == "Easy":
            ai_move_easy()
        elif st.session_state.difficulty == "Medium":
            ai_move_medium()
        else:  # Hard
            ai_move_minimax()
        
        # Check if the game is over after AI's move
        if check_winner(st.session_state.ttt_board, 'O'):
            st.session_state.game_over = True
            st.session_state.winner = 'O'
        elif is_full(st.session_state.ttt_board):
            st.session_state.game_over = True
            st.session_state.winner = None
        
        # Human's turn again
        st.session_state.human_turn = True
        
        # Rerun to update the UI
        st.rerun()

def check_winner(board, player):
    # Check rows
    for i in range(3):
        if np.all(board[i, :] == player):
            return True
    
    # Check columns
    for i in range(3):
        if np.all(board[:, i] == player):
            return True
    
    # Check diagonals
    if board[0, 0] == board[1, 1] == board[2, 2] == player:
        return True
    if board[0, 2] == board[1, 1] == board[2, 0] == player:
        return True
    
    return False

def is_full(board):
    return ' ' not in board

def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i, j] == ' ':
                empty_cells.append((i, j))
    return empty_cells

def ai_move_easy():
    """AI makes a random move"""
    empty_cells = get_empty_cells(st.session_state.ttt_board)
    if empty_cells:
        i, j = random.choice(empty_cells)
        st.session_state.ttt_board[i, j] = 'O'

def ai_move_medium():
    """
    AI with medium difficulty:
    1. If AI can win in the next move, make that move
    2. If player can win in the next move, block that move
    3. Otherwise, make a random move
    """
    board = st.session_state.ttt_board.copy()
    empty_cells = get_empty_cells(board)
    
    # Check if AI can win in the next move
    for i, j in empty_cells:
        board[i, j] = 'O'
        if check_winner(board, 'O'):
            st.session_state.ttt_board[i, j] = 'O'
            return
        board[i, j] = ' '  # Reset
    
    # Check if player can win in the next move and block
    for i, j in empty_cells:
        board[i, j] = 'X'
        if check_winner(board, 'X'):
            st.session_state.ttt_board[i, j] = 'O'
            return
        board[i, j] = ' '  # Reset
    
    # Make a random move
    ai_move_easy()

def minimax(board, depth, is_maximizing):
    """Minimax algorithm for unbeatable AI"""
    # Check terminal states
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_full(board):
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i, j] == ' ':
                    board[i, j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i, j] = ' '  # Reset
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i, j] == ' ':
                    board[i, j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i, j] = ' '  # Reset
                    best_score = min(score, best_score)
        return best_score

def ai_move_minimax():
    """Make the best move using minimax algorithm"""
    best_score = float('-inf')
    best_move = None
    board = st.session_state.ttt_board.copy()
    
    for i in range(3):
        for j in range(3):
            if board[i, j] == ' ':
                board[i, j] = 'O'
                score = minimax(board, 0, False)
                board[i, j] = ' '  # Reset
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    if best_move:
        i, j = best_move
        st.session_state.ttt_board[i, j] = 'O'