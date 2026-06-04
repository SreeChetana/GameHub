import streamlit as st
import random
import time
from utils import display_game_time

def display_connect4_board(board):
    symbol_map = {
        0: "⚪",  # Empty
        1: "🔴",  # Player 1
        2: "🟡"   # Player 2 (AI or Player 2)
    }
    for row in board:
        st.markdown("".join(symbol_map[cell] for cell in row), unsafe_allow_html=True)

def render_connect4():
    st.title("Connect 4")

    if st.session_state.game_start_time is None:
        st.session_state.game_start_time = time.time()

    mode = st.radio("Mode", ["Human vs Human", "Human vs AI"])
    game_state = st.session_state.games['connect4']

    if st.button("Reset Game"):
        game_state['board'] = [[0 for _ in range(7)] for _ in range(6)]
        game_state['current_player'] = 1
        game_state['winner'] = None
        st.session_state.game_start_time = time.time()
        st.experimental_rerun()

    # Display board
    st.write("Current Board:")
    display_connect4_board(game_state['board'])

    if game_state['winner']:
        st.success(f"Player {game_state['winner']} wins!")
        update_leaderboard('connect4', game_state['winner'])
    elif check_draw(game_state['board']):
        st.info("It's a draw!")
    else:
        st.write(f"Current player: {'Red (🔴)' if game_state['current_player'] == 1 else 'Yellow (🟡)'}")

        # Column buttons
        cols = st.columns(7)
        for col in range(7):
            with cols[col]:
                if st.button(f"↓", key=f"c4_col_{col}", disabled=game_state['winner'] is not None):
                    if make_connect4_move(game_state, col):
                        if check_connect4_win(game_state['board'], game_state['current_player']):
                            game_state['winner'] = game_state['current_player']
                        elif check_draw(game_state['board']):
                            pass  # Handled above
                        else:
                            game_state['current_player'] = 3 - game_state['current_player']

                            # AI Move if needed
                            if mode == "Human vs AI" and game_state['current_player'] == 2:
                                ai_move_connect4(game_state)
                                if check_connect4_win(game_state['board'], 2):
                                    game_state['winner'] = 2
                                elif check_draw(game_state['board']):
                                    pass
                                else:
                                    game_state['current_player'] = 1
                        st.experimental_rerun()

    display_game_time()

def make_connect4_move(game_state, col):
    board = game_state['board']
    for row in range(5, -1, -1):
        if board[row][col] == 0:
            board[row][col] = game_state['current_player']
            return True
    return False

def check_connect4_win(board, player):
    # Horizontal
    for row in range(6):
        for col in range(4):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    # Vertical
    for row in range(3):
        for col in range(7):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    # Diagonal (\)
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    # Diagonal (/)
    for row in range(3, 6):
        for col in range(4):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][col] != 0 for col in range(7))

def ai_move_connect4(game_state):
    board = game_state['board']
    best_score = -float('inf')
    best_col = None

    for col in range(7):
        if all(board[row][col] != 0 for row in range(6)):
            continue
        for row in range(5, -1, -1):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax_connect4(board, 3, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_col = col
                break

    if best_col is not None:
        make_connect4_move(game_state, best_col)

def minimax_connect4(board, depth, is_maximizing):
    if check_connect4_win(board, 2):
        return 10
    if check_connect4_win(board, 1):
        return -10
    if depth == 0 or all(board[0][col] != 0 for col in range(7)):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for col in range(7):
            if all(board[row][col] != 0 for row in range(6)):
                continue
            for row in range(5, -1, -1):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax_connect4(board, depth - 1, False)
                    board[row][col] = 0
                    best_score = max(best_score, score)
                    break
        return best_score
    else:
        best_score = float('inf')
        for col in range(7):
            if all(board[row][col] != 0 for row in range(6)):
                continue
            for row in range(5, -1, -1):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax_connect4(board, depth - 1, True)
                    board[row][col] = 0
                    best_score = min(best_score, score)
                    break
        return best_score
