# games/sudoku.py

import streamlit as st
import random
import time

def render_sudoku():
    st.title("Sudoku Solver & Player")

    if 'games' not in st.session_state or 'sudoku' not in st.session_state.games:
        st.error("Session state for Sudoku not found.")
        return

    game_state = st.session_state.games['sudoku']

    colA, colB = st.columns(2)
    with colA:
        if st.button("🔁 New Game"):
            game_state['board'] = generate_sudoku()
            game_state['original'] = [row[:] for row in game_state['board']]
            game_state['solution'] = None
            st.session_state.game_start_time = time.time()
            st.rerun()

    with colB:
        if st.button("🧠 Solve"):
            game_state['solution'] = [row[:] for row in game_state['board']]
            if solve_sudoku(game_state['solution']):
                st.success("Sudoku solved successfully!")
            else:
                st.error("No solution exists.")

    if game_state['board'] is None or game_state['original'] is None:
        st.warning("Click 'New Game' to start playing.")
        return

    st.subheader("🎮 Current Board:")
    display_sudoku_board(game_state['board'], game_state['original'])

    if game_state['solution']:
        st.subheader("✅ Solution:")
        display_sudoku_board(game_state['solution'], None)

    st.markdown("---")
    st.subheader("✍️ Make a Move")

    col1, col2, col3 = st.columns(3)
    with col1:
        row = st.selectbox("Row", range(1, 10)) - 1
    with col2:
        col = st.selectbox("Column", range(1, 10)) - 1
    with col3:
        value = st.selectbox("Value (0 to clear)", range(0, 10))

    if st.button("📥 Place Number"):
        if game_state['original'][row][col] != 0:
            st.error("You can't modify original numbers!")
        else:
            game_state['board'][row][col] = value
            st.rerun()

    display_game_time()

# --- Sudoku Logic ---

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    for _ in range(40):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
    return board

def solve_sudoku(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, row, col, num):
    if num in board[row]: return False
    if num in [board[i][col] for i in range(9)]: return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def display_sudoku_board(board, original):
    html = """
    <style>
    .sudoku-grid {
        display: grid;
        grid-template-columns: repeat(9, 50px);
        border: 3px solid black;
    }
    .sudoku-cell {
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        font-family: monospace;
        color: #000000;
        border: 1px solid #999;
    }
    </style>
    <div class="sudoku-grid">
    """
    for i in range(9):
        for j in range(9):
            value = board[i][j] if board[i][j] != 0 else ""
            bg = "#f8f8f8" if original is None or original[i][j] == 0 else "#cccccc"
            weight = "bold" if original and original[i][j] != 0 else "normal"
            border_style = ""
            if j % 3 == 0:
                border_style += "border-left: 3px solid black;"
            if i % 3 == 0:
                border_style += "border-top: 3px solid black;"
            if j == 8:
                border_style += "border-right: 3px solid black;"
            if i == 8:
                border_style += "border-bottom: 3px solid black;"
            html += f"<div class='sudoku-cell' style='background-color: {bg}; font-weight: {weight}; {border_style}'>{value}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def display_game_time():
    if 'game_start_time' in st.session_state:
        elapsed = int(time.time() - st.session_state.game_start_time)
        mins, secs = divmod(elapsed, 60)
        st.info(f"⏱️ Time Elapsed: {mins:02d}:{secs:02d}")
