import streamlit as st
import time
from utils import display_game_time
from leaderboard import update_leaderboard

def render_n_queens():
    st.title("N-Queens Puzzle")
    
    # Initialize game state with all required keys
    if 'n_queens' not in st.session_state.games:
        st.session_state.games['n_queens'] = {
            'size': 8,
            'solutions': [],
            'current_solution': 0,
            'user_board': None,
            'mode': 'visualize'
        }
    
    game_state = st.session_state.games['n_queens']
    
    # Ensure all keys exist (backward compatibility)
    if 'mode' not in game_state:
        game_state['mode'] = 'visualize'
    if 'user_board' not in game_state:
        game_state['user_board'] = None
    
    # Mode selection
    mode = st.radio("Select mode", ["Visualize Solutions", "Play Yourself"], 
                   index=0 if game_state['mode'] == 'visualize' else 1)
    
    # Update mode in game state
    game_state['mode'] = 'visualize' if mode == "Visualize Solutions" else 'play'
    
    size = st.slider("Board size", 4, 12, game_state['size'])
    
    if game_state['mode'] == 'visualize':
        if st.button("Find Solutions") or game_state['size'] != size:
            game_state['size'] = size
            game_state['solutions'] = solve_n_queens(size)
            game_state['current_solution'] = 0
            st.session_state.game_start_time = time.time()
        
        if game_state['solutions']:
            st.write(f"Solution {game_state['current_solution'] + 1} of {len(game_state['solutions'])}")
            display_queens_board(game_state['solutions'][game_state['current_solution']])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous Solution") and game_state['current_solution'] > 0:
                    game_state['current_solution'] -= 1
                    st.rerun()
            with col2:
                if st.button("Next Solution") and game_state['current_solution'] < len(game_state['solutions']) - 1:
                    game_state['current_solution'] += 1
                    st.rerun()
    else:
        # Play mode
        if game_state['size'] != size or game_state['user_board'] is None:
            game_state['size'] = size
            game_state['user_board'] = [[0 for _ in range(size)] for _ in range(size)]
            st.session_state.game_start_time = time.time()
        
        st.write("Place queens on the board (click on squares). Try to place all queens without them attacking each other!")
        
        # Display interactive board
        display_interactive_board(game_state['user_board'])
        
        # Check if the current placement is valid
        if is_valid_solution(game_state['user_board']):
            st.success("Congratulations! You've solved the N-Queens puzzle!")
            update_leaderboard('n_queens', st.session_state.player_name, 1)
        else:
            queens_placed = sum(sum(row) for row in game_state['user_board'])
            st.write(f"Queens placed: {queens_placed}/{size}")
            
            if queens_placed == size:
                st.error("Some queens are attacking each other. Try again!")
        
        if st.button("Reset Board"):
            game_state['user_board'] = [[0 for _ in range(size)] for _ in range(size)]
            st.rerun()
    
    display_game_time()

def solve_n_queens(size):
    solutions = []
    
    def is_safe(board, row, col):
        # Check this row on left side
        for i in range(col):
            if board[row][i] == 1:
                return False
        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        # Check lower diagonal on left side
        for i, j in zip(range(row, size, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True
    
    def solve(board, col):
        if col >= size:
            solutions.append([row[:] for row in board])
            return
        for i in range(size):
            if is_safe(board, i, col):
                board[i][col] = 1
                solve(board, col + 1)
                board[i][col] = 0
    
    board = [[0 for _ in range(size)] for _ in range(size)]
    solve(board, 0)
    return solutions

def display_queens_board(solution):
    size = len(solution)
    html = "<div style='display: grid; grid-template-columns: repeat(" + str(size) + ", 50px);'>"
    for row in range(size):
        for col in range(size):
            color = "#eee" if (row + col) % 2 == 0 else "#999"
            text_color = "#000" if color == "#eee" else "#fff"
            content = f"<span style='color:{text_color}'>♕</span>" if solution[row][col] == 1 else ""
            html += f"<div style='width: 50px; height: 50px; background-color: {color}; display: flex; justify-content: center; align-items: center; font-size: 30px;'>{content}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def display_interactive_board(board):
    size = len(board)
    cols = st.columns(size)
    
    for row in range(size):
        for col in range(size):
            color = "#eee" if (row + col) % 2 == 0 else "#999"
            text_color = "#000" if color == "#eee" else "#fff"
            queen = board[row][col] == 1
            content = "♕" if queen else ""
            
            with cols[col]:
                if st.button(
                    content,
                    key=f"queen_{row}_{col}",
                    help=f"Row {row+1}, Col {col+1}",
                    on_click=toggle_queen,
                    args=(row, col, board)
                ):
                    pass
    
    # Add CSS styling for the buttons
    st.markdown("""
    <style>
        div[data-testid="stButton"] > button[kind="secondary"] {
            width: 50px;
            height: 50px;
            padding: 0;
            margin: 0;
            font-size: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: var(--background-color);
            color: var(--text-color);
        }
    </style>
    """, unsafe_allow_html=True)
    
    return board

def toggle_queen(row, col, board):
    # Toggle queen presence (1 becomes 0, 0 becomes 1)
    board[row][col] = 1 - board[row][col]

def is_valid_solution(board):
    size = len(board)
    queens = []
    
    # Find all queen positions
    for row in range(size):
        for col in range(size):
            if board[row][col] == 1:
                queens.append((row, col))
    
    # Check if any queens attack each other
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            row1, col1 = queens[i]
            row2, col2 = queens[j]
            
            # Same row or column
            if row1 == row2 or col1 == col2:
                return False
            # Same diagonal
            if abs(row1 - row2) == abs(col1 - col2):
                return False
                
    return len(queens) == size