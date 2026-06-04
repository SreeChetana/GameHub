import streamlit as st
import time

def display_game_time():
    if st.session_state.game_start_time:
        elapsed_time = int(time.time() - st.session_state.game_start_time)
        st.write(f"Time: {elapsed_time // 60}m {elapsed_time % 60}s")
