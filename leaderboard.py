import streamlit as st
import pandas as pd
import time

def update_leaderboard(game, player_name, value=1):
    if player_name == 'Player':
        return
        
    if game not in st.session_state.leaderboard:
        st.session_state.leaderboard[game] = {'scores': {}, 'times': {}}
    
    # Determine the correct metric based on game type
    if game in ['tic_tac_toe', 'connect4', 'hangman']:
        metric = 'wins'
    elif game == '2048':
        metric = 'high_scores'
    elif game == 'maze':
        metric = 'completions'
    else:  # n_queens and others
        metric = 'solutions'
    
    # Update the metric
    if player_name in st.session_state.leaderboard[game][metric]:
        if game == '2048':
            st.session_state.leaderboard[game][metric][player_name] = max(
                st.session_state.leaderboard[game][metric][player_name], value)
        else:
            st.session_state.leaderboard[game][metric][player_name] += value
    else:
        st.session_state.leaderboard[game][metric][player_name] = value
    
    # Update time
    st.session_state.leaderboard[game]['times'][player_name] = time.strftime("%Y-%m-%d %H:%M:%S")

def display_leaderboard():
    st.title("Leaderboard")
    
    if not st.session_state.leaderboard:
        st.warning("No leaderboard data available yet!")
        return
    
    game = st.selectbox("Select Game", list(st.session_state.leaderboard.keys()))
    
    if game in ['tic_tac_toe', 'connect4', 'hangman']:
        metric = 'wins'
        title = "Wins"
    elif game == '2048':
        metric = 'high_scores'
        title = "High Scores"
    elif game == 'maze':
        metric = 'completions'
        title = "Completions"
    else:  # n_queens and others
        metric = 'solutions'
        title = "Solutions Found"
    
    if st.session_state.leaderboard[game][metric]:
        df = pd.DataFrame.from_dict(
            st.session_state.leaderboard[game][metric], 
            orient='index',
            columns=[title]
        )
        df['Last Played'] = pd.Series(st.session_state.leaderboard[game]['times'])
        st.dataframe(df.sort_values(title, ascending=False))
    else:
        st.info(f"No {title.lower()} recorded yet for {game.replace('_', ' ')}")