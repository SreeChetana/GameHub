import streamlit as st
import random
import time

def render_2048():
    st.title("2048")
    
    if st.session_state.game_start_time is None:
        st.session_state.game_start_time = time.time()
    
    game_state = st.session_state.games['2048']
    
    if st.button("New Game"):
        game_state['board'] = initialize_2048()
        game_state['score'] = 0
        game_state['game_over'] = False
        st.session_state.game_start_time = time.time()
        st.experimental_rerun()
    
    st.write(f"Score: {game_state['score']}")
    display_2048_board(game_state['board'])
    
    if game_state['game_over']:
        st.error("Game Over!")
        update_leaderboard('2048', st.session_state.player_name, score=game_state['score'])
        if st.button("Play Again"):
            game_state['board'] = initialize_2048()
            game_state['score'] = 0
            game_state['game_over'] = False
            st.session_state.game_start_time = time.time()
            st.experimental_rerun()
    else:
        # Movement controls
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            if st.button("↑", key="2048_up"):
                move_2048(game_state, 'up')
        with col1:
            if st.button("←", key="2048_left"):
                move_2048(game_state, 'left')
        with col3:
            if st.button("→", key="2048_right"):
                move_2048(game_state, 'right')
        with col4:
            if st.button("↓", key="2048_down"):
                move_2048(game_state, 'down')
    
    display_game_time()

def initialize_2048():
    board = [[0 for _ in range(4)] for _ in range(4)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def move_2048(game_state, direction):
    board = game_state['board']
    moved = False
    score = 0
    
    if direction == 'left':
        for row in range(4):
            # Remove zeros
            non_zeros = [cell for cell in board[row] if cell != 0]
            # Merge adjacent equal numbers
            i = 0
            while i < len(non_zeros) - 1:
                if non_zeros[i] == non_zeros[i+1]:
                    non_zeros[i] *= 2
                    score += non_zeros[i]
                    non_zeros.pop(i+1)
                i += 1
            # Pad with zeros
            new_row = non_zeros + [0] * (4 - len(non_zeros))
            if new_row != board[row]:
                moved = True
            board[row] = new_row
    
    elif direction == 'right':
        for row in range(4):
            non_zeros = [cell for cell in board[row] if cell != 0]
            i = len(non_zeros) - 1
            while i > 0:
                if non_zeros[i] == non_zeros[i-1]:
                    non_zeros[i] *= 2
                    score += non_zeros[i]
                    non_zeros.pop(i-1)
                    i -= 1
                i -= 1
            new_row = [0] * (4 - len(non_zeros)) + non_zeros
            if new_row != board[row]:
                moved = True
            board[row] = new_row
    
    elif direction == 'up':
        for col in range(4):
            column = [board[row][col] for row in range(4)]
            non_zeros = [cell for cell in column if cell != 0]
            i = 0
            while i < len(non_zeros) - 1:
                if non_zeros[i] == non_zeros[i+1]:
                    non_zeros[i] *= 2
                    score += non_zeros[i]
                    non_zeros.pop(i+1)
                i += 1
            new_column = non_zeros + [0] * (4 - len(non_zeros))
            for row in range(4):
                if board[row][col] != new_column[row]:
                    moved = True
                board[row][col] = new_column[row]
    
    elif direction == 'down':
        for col in range(4):
            column = [board[row][col] for row in range(4)]
            non_zeros = [cell for cell in column if cell != 0]
            i = len(non_zeros) - 1
            while i > 0:
                if non_zeros[i] == non_zeros[i-1]:
                    non_zeros[i] *= 2
                    score += non_zeros[i]
                    non_zeros.pop(i-1)
                    i -= 1
                i -= 1
            new_column = [0] * (4 - len(non_zeros)) + non_zeros
            for row in range(4):
                if board[row][col] != new_column[row]:
                    moved = True
                board[row][col] = new_column[row]
    
    game_state['score'] += score
    
    if moved:
        add_random_tile(board)
        
        # Check for game over
        if check_2048_game_over(board):
            game_state['game_over'] = True
    
    return moved

def check_2048_game_over(board):
    # Check if there are any empty cells
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                return False
    
    # Check if there are any adjacent equal cells
    for row in range(4):
        for col in range(3):
            if board[row][col] == board[row][col+1]:
                return False
    
    for col in range(4):
        for row in range(3):
            if board[row][col] == board[row+1][col]:
                return False
    
    return True

def display_2048_board(board):
    colors = {
        0: "#ccc0b3",
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e"
    }
    
    html = "<div style='display: grid; grid-template-columns: repeat(4, 80px); gap: 10px; background-color: #bbada0; padding: 10px; border-radius: 5px;'>"
    for row in range(4):
        for col in range(4):
            value = board[row][col]
            color = colors.get(value, "#000000")
            text_color = "#776e65" if value <= 4 else "#f9f6f2"
            font_size = "24px" if value < 100 else "20px" if value < 1000 else "16px"
            text = str(value) if value != 0 else ""
            html += f"<div style='width: 80px; height: 80px; background-color: {color}; color: {text_color}; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: {font_size};'>{text}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def display_game_time():
    if st.session_state.game_start_time:
        elapsed_time = int(time.time() - st.session_state.game_start_time)
        st.write(f"Time: {elapsed_time // 60}m {elapsed_time % 60}s")

def update_leaderboard(game, player_name, score=1):
    if player_name not in st.session_state.leaderboard[game]['wins']:
        st.session_state.leaderboard[game]['wins'][player_name] = 0
        st.session_state.leaderboard[game]['times'][player_name] = []
    
    st.session_state.leaderboard[game]['wins'][player_name] += score
    
    if st.session_state.game_start_time:
        elapsed_time = int(time.time() - st.session_state.game_start_time)
        st.session_state.leaderboard[game]['times'][player_name].append(elapsed_time)
