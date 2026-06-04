import streamlit as st
import pandas as pd
import time

# Import game modules
from games.tic_tac_toe import render_tic_tac_toe
from games.n_queens import render_n_queens
from games.sudoku import render_sudoku
from games.connect4 import render_connect4
from games.game_2048 import render_2048, initialize_2048
from games.hangman import render_hangman
from games.maze import render_maze
from leaderboard import display_leaderboard, update_leaderboard

# Initialize session state
if 'games' not in st.session_state:
    st.session_state.games = {
        'tic_tac_toe': {'board': [[' ' for _ in range(3)] for _ in range(3)], 'current_player': 'X', 'winner': None},
        'n_queens': {
            'size': 8,
            'solutions': [],
            'current_solution': 0,
            'user_board': None,
            'mode': 'visualize'
        },
        'sudoku': {'board': [[0 for _ in range(9)] for _ in range(9)], 'original': None, 'solution': None},
        'connect4': {'board': [[0 for _ in range(7)] for _ in range(6)], 'current_player': 1, 'winner': None},
        '2048': {'board': initialize_2048(), 'score': 0, 'game_over': False},
        'hangman': {'word': '', 'guessed': [], 'wrong_guesses': 0, 'max_wrong': 6},
        'maze': {'grid': None, 'start': None, 'end': None, 'player_pos': None, 'path': None, 'size': 10}
    }

if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = {
        'tic_tac_toe': {'wins': {}, 'times': {}},
        'connect4': {'wins': {}, 'times': {}},
        '2048': {'high_scores': {}, 'times': {}},  # Changed from 'scores' to 'high_scores'
        'hangman': {'wins': {}, 'times': {}},
        'maze': {'completions': {}, 'times': {}},  # Changed from 'scores' to 'completions'
        'n_queens': {'solutions': {}, 'times': {}}  # Changed from 'wins' to 'solutions'
    }

if 'current_game' not in st.session_state:
    st.session_state.current_game = None

if 'player_name' not in st.session_state:
    st.session_state.player_name = 'Player'

if 'game_start_time' not in st.session_state:
    st.session_state.game_start_time = None

def render_home():
    st.title("Welcome to the Game Center")
    st.write("""
    This application offers several classic games for you to enjoy. 
    Select a game from the sidebar to get started.
    """)
    
    st.subheader("Available Games:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("- Tic Tac Toe")
        st.write("- N-Queens Puzzle")
        st.write("- Sudoku")
        st.write("- Connect 4")
    
    with col2:
        st.write("- 2048")
        st.write("- Hangman")
        st.write("- Maze Runner")
    
    st.subheader("How to Play")
    st.write("""
    1. Enter your name in the sidebar
    2. Select a game from the dropdown menu
    3. Follow the instructions for each game
    4. Your scores will be saved to the leaderboard
    """)

def main():
    st.sidebar.title("Game Center")
    
    # Player name input
    player_name = st.sidebar.text_input("Your Name:", value=st.session_state.player_name)
    if player_name != st.session_state.player_name:
        st.session_state.player_name = player_name
    
    # Game selection
    game_options = {
        "Home": "home",
        "Tic Tac Toe": "tic_tac_toe",
        "N-Queens Puzzle": "n_queens",
        "Sudoku": "sudoku",
        "Connect 4": "connect4",
        "2048": "2048",
        "Hangman": "hangman",
        "Maze Runner": "maze",
        "Leaderboard": "leaderboard"
    }
    
    selected_game = st.sidebar.selectbox("Select Game", list(game_options.keys()))
    
    if game_options[selected_game] != st.session_state.current_game:
        st.session_state.current_game = game_options[selected_game]
        st.session_state.game_start_time = time.time()  # Reset timer when switching games
    
    # Render selected game
    if st.session_state.current_game == "home":
        render_home()
    elif st.session_state.current_game == "tic_tac_toe":
        render_tic_tac_toe()
    elif st.session_state.current_game == "n_queens":
        render_n_queens()
    elif st.session_state.current_game == "sudoku":
        render_sudoku()
    elif st.session_state.current_game == "connect4":
        render_connect4()
    elif st.session_state.current_game == "2048":
        render_2048()
    elif st.session_state.current_game == "hangman":
        render_hangman()
    elif st.session_state.current_game == "maze":
        render_maze()
    elif st.session_state.current_game == "leaderboard":
        display_leaderboard()

if __name__ == "__main__":
    main()