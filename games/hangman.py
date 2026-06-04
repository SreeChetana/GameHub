import streamlit as st
import random
import time

# Word dictionary with clues
WORD_CLUES = {
    "python": "A popular programming language named after a snake",
    "streamlit": "A framework for creating web apps with Python",
    "game": "An activity engaged in for amusement",
    "computer": "An electronic device for processing data",
    "algorithm": "A set of rules to solve a problem",
    "artificial": "Made by human beings rather than occurring naturally",
    "intelligence": "The ability to acquire and apply knowledge",
    "hangman": "The name of this game",
    "keyboard": "Input device with keys",
    "developer": "A person who writes software"
}

def render_hangman():
    st.title("Hangman")
    
    # Initialize game state if not exists
    if 'games' not in st.session_state:
        st.session_state.games = {}
    if 'hangman' not in st.session_state.games:
        st.session_state.games['hangman'] = {
            'word': '',
            'guessed': [],
            'wrong_guesses': 0,
            'max_wrong': 6,  # 6 body parts = head, body, 2 arms, 2 legs
            'clue': ''
        }
    
    # Initialize game time if not exists
    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = None
    
    game_state = st.session_state.games['hangman']
    
    # Display instructions
    st.write("""
    **Instructions:**
    - Guess the hidden word one letter at a time
    - You can make up to 6 wrong guesses before losing
    - Each wrong guess adds a part to the hangman figure
    - Use the clue to help you guess the word
    - Type a letter and click Guess to make your guess
    """)
    
    # Start new game if no word or New Game button pressed
    if not game_state['word'] or st.button("New Game"):
        word = random.choice(list(WORD_CLUES.keys()))
        game_state['word'] = word
        game_state['clue'] = WORD_CLUES[word]
        game_state['guessed'] = []
        game_state['wrong_guesses'] = 0
        st.session_state.game_start_time = time.time()
        st.rerun()
    
    # Display hangman figure
    display_hangman_figure(game_state['wrong_guesses'])
    
    # Display the clue
    st.write(f"**Clue:** {game_state['clue']}")
    
    # Display word with guessed letters
    display_word = ""
    all_guessed = True
    for char in game_state['word']:
        if char in game_state['guessed']:
            display_word += char + " "
        else:
            display_word += "_ "
            all_guessed = False
    
    st.subheader(display_word)
    st.write(f"Guessed letters: {', '.join(sorted(game_state['guessed']))}")
    
    # Check for win/loss
    if all_guessed:
        st.success("Congratulations! You Win!")
        update_leaderboard('hangman', st.session_state.player_name)
        
        if st.button("Play Again"):
            word = random.choice(list(WORD_CLUES.keys()))
            game_state['word'] = word
            game_state['clue'] = WORD_CLUES[word]
            game_state['guessed'] = []
            game_state['wrong_guesses'] = 0
            st.session_state.game_start_time = time.time()
            st.rerun()
            
    elif game_state['wrong_guesses'] >= game_state['max_wrong']:
        st.error(f"Game Over! The word was: {game_state['word']}")
        
        if st.button("Try Again"):
            word = random.choice(list(WORD_CLUES.keys()))
            game_state['word'] = word
            game_state['clue'] = WORD_CLUES[word]
            game_state['guessed'] = []
            game_state['wrong_guesses'] = 0
            st.session_state.game_start_time = time.time()
            st.rerun()
    else:
        # Guess input
        col1, col2 = st.columns([1, 3])
        with col1:
            letter = st.text_input("Guess a letter:", max_chars=1, key="hangman_guess").lower()
        with col2:
            st.write("")  # For alignment
            if st.button("Guess", key="hangman_guess_btn"):
                if letter and letter.isalpha() and letter not in game_state['guessed']:
                    game_state['guessed'].append(letter)
                    if letter not in game_state['word']:
                        game_state['wrong_guesses'] += 1
                    st.rerun()
                elif letter in game_state['guessed']:
                    st.warning("You already guessed that letter!")
    
    display_game_time()

def display_hangman_figure(wrong_guesses):
    hangman_pics = [
        """
          +---+
          |   |
              |
              |
              |
              |
        =========""",
        """
          +---+
          |   |
          O   |
              |
              |
              |
        =========""",
        """
          +---+
          |   |
          O   |
          |   |
              |
              |
        =========""",
        """
          +---+
          |   |
          O   |
         /|   |
              |
              |
        =========""",
        """
          +---+
          |   |
          O   |
         /|\  |
              |
              |
        =========""",
        """
          +---+
          |   |
          O   |
         /|\  |
         /    |
              |
        =========""",
        """
          +---+
          |   |
          O   |
         /|\  |
         / \  |
              |
        ========="""
    ]
    st.text(hangman_pics[min(wrong_guesses, len(hangman_pics)-1)])

def display_game_time():
    if st.session_state.game_start_time:
        elapsed_time = int(time.time() - st.session_state.game_start_time)
        st.write(f"Time: {elapsed_time // 60}m {elapsed_time % 60}s")

def update_leaderboard(game, player_name, score=1):
    # Initialize leaderboard if not exists
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = {}
    if game not in st.session_state.leaderboard:
        st.session_state.leaderboard[game] = {'wins': {}, 'times': {}}
    
    if player_name not in st.session_state.leaderboard[game]['wins']:
        st.session_state.leaderboard[game]['wins'][player_name] = 0
        st.session_state.leaderboard[game]['times'][player_name] = []
    
    st.session_state.leaderboard[game]['wins'][player_name] += score
    
    if st.session_state.game_start_time:
        elapsed_time = int(time.time() - st.session_state.game_start_time)
        st.session_state.leaderboard[game]['times'][player_name].append(elapsed_time)
