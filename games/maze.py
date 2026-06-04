import streamlit as st
import random
import time
from collections import deque

def generate_maze(size):
    # Ensure size is odd to make the maze work properly
    if size % 2 == 0:
        size += 1
    
    # Create a grid filled with walls
    grid = [['#' for _ in range(size)] for _ in range(size)]
    
    def carve_passages(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and grid[ny][nx] == '#':
                grid[ny][nx] = '.'
                grid[y + dy//2][x + dx//2] = '.'
                carve_passages(nx, ny)
    
    # Start with a random point and carve passages
    start_x, start_y = random.randrange(1, size, 2), random.randrange(1, size, 2)
    grid[start_y][start_x] = '.'
    carve_passages(start_x, start_y)
    
    # Find suitable start and end points
    potential_starts = []
    for y in range(size):
        for x in range(size):
            if grid[y][x] == '.':
                potential_starts.append((x, y))
    
    if not potential_starts:
        return generate_maze(size)  # Try again if no paths were generated
    
    start_point = random.choice(potential_starts)
    
    # Find a point far from the start point
    max_dist = 0
    end_point = start_point
    for point in potential_starts:
        dist = abs(point[0] - start_point[0]) + abs(point[1] - start_point[1])
        if dist > max_dist:
            max_dist = dist
            end_point = point
    
    return grid, start_point, end_point

def solve_maze(grid, start, end):
    size = len(grid)
    visited = [[False for _ in range(size)] for _ in range(size)]
    queue = deque([(start, [])])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == end:
            return path + [(x, y)]
        
        if visited[y][x]:
            continue
        
        visited[y][x] = True
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and grid[ny][nx] == '.' and not visited[ny][nx]:
                queue.append(((nx, ny), path + [(x, y)]))
    
    return []

def move_player(game_state, direction):
    x, y = game_state['player_pos']
    dx, dy = 0, 0
    
    if direction == 'up':
        dy = -1
    elif direction == 'down':
        dy = 1
    elif direction == 'left':
        dx = -1
    elif direction == 'right':
        dx = 1
    
    nx, ny = x + dx, y + dy
    size = len(game_state['grid'])
    
    if 0 <= nx < size and 0 <= ny < size and game_state['grid'][ny][nx] == '.':
        game_state['player_pos'] = (nx, ny)
        return True
    return False

def display_maze(game_state):
    grid = game_state['grid']
    size = len(grid)
    
    html = "<div style='display: grid; grid-template-columns: repeat(" + str(size) + ", 25px); gap: 0;'>"
    for y in range(size):
        for x in range(size):
            if game_state['player_pos'] == (x, y):
                color = "#ff0000"  # Red for player
            elif game_state['start'] == (x, y):
                color = "#00ff00"  # Green for start
            elif game_state['end'] == (x, y):
                color = "#0000ff"  # Blue for end
            elif (x, y) in game_state['path']:
                color = "#ffff00"  # Yellow for solution path
            else:
                color = "#ffffff" if grid[y][x] == '.' else "#000000"
            
            html += f"<div style='width: 25px; height: 25px; background-color: {color};'></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def render_maze():
    st.title("Maze Runner")
    
    # Initialize game state if not exists
    if 'games' not in st.session_state:
        st.session_state.games = {}
    if 'maze' not in st.session_state.games:
        st.session_state.games['maze'] = {
            'size': 15,
            'grid': None,
            'start': None,
            'end': None,
            'player_pos': None,
            'path': []
        }
    
    # Initialize leaderboard if not exists
    if 'leaderboard' not in st.session_state:
        st.session_state.leaderboard = {}
    if 'maze' not in st.session_state.leaderboard:
        st.session_state.leaderboard['maze'] = {'scores': {}, 'times': {}}
    
    # Initialize player name if not exists
    if 'player_name' not in st.session_state:
        st.session_state.player_name = "Player"
    
    # Get the maze state from session state
    game_state = st.session_state.games['maze']
    
    # Maze size configuration
    maze_size = st.sidebar.slider("Maze Size", 5, 31, game_state['size'], step=2)
    if maze_size != game_state['size']:
        game_state['size'] = maze_size
    
    if st.button("Generate New Maze") or game_state['grid'] is None:
        size = game_state['size']
        game_state['grid'], game_state['start'], game_state['end'] = generate_maze(size)
        game_state['player_pos'] = game_state['start']
        game_state['path'] = []
        st.session_state.game_start_time = time.time()
        st.rerun()
    
    # Display instructions
    st.write("""
    **Instructions:**
    - Navigate from the green start point to the blue end point
    - Use the arrow buttons to move
    - White spaces are paths, black spaces are walls
    - You can use "Show Solution" if you get stuck
    """)
    
    # Display maze
    if game_state['grid'] is not None:
        display_maze(game_state)
    
    # Movement controls
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        move_buttons = st.columns(4)
        with move_buttons[1]:
            if st.button("↑", key="maze_up"):
                if move_player(game_state, 'up'):
                    st.rerun()
        
        with move_buttons[0]:
            if st.button("←", key="maze_left"):
                if move_player(game_state, 'left'):
                    st.rerun()
        
        with move_buttons[2]:
            if st.button("→", key="maze_right"):
                if move_player(game_state, 'right'):
                    st.rerun()
        
        with move_buttons[3]:
            if st.button("↓", key="maze_down"):
                if move_player(game_state, 'down'):
                    st.rerun()
    
    # Check for win
    if game_state['player_pos'] == game_state['end'] and game_state['grid'] is not None:
        st.success("Congratulations! You solved the maze!")
        
        # Update leaderboard
        player_name = st.session_state.player_name
        
        if player_name not in st.session_state.leaderboard['maze']['scores']:
            st.session_state.leaderboard['maze']['scores'][player_name] = 0
            st.session_state.leaderboard['maze']['times'][player_name] = []
        
        st.session_state.leaderboard['maze']['scores'][player_name] += 1
        
        if 'game_start_time' in st.session_state:
            elapsed_time = int(time.time() - st.session_state.game_start_time)
            st.session_state.leaderboard['maze']['times'][player_name].append(elapsed_time)
        
        if st.button("Play Again"):
            game_state['grid'], game_state['start'], game_state['end'] = generate_maze(game_state['size'])
            game_state['player_pos'] = game_state['start']
            game_state['path'] = []
            st.session_state.game_start_time = time.time()
            st.rerun()
    
    # Show solution button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show Solution") and game_state['grid'] is not None:
            game_state['path'] = solve_maze(game_state['grid'], game_state['start'], game_state['end'])
            st.rerun()
    
    with col2:
        if st.button("Hide Solution"):
            game_state['path'] = []
            st.rerun()
    
    # Display game time
    if 'game_start_time' in st.session_state and game_state['grid'] is not None:
        elapsed_time = int(time.time() - st.session_state.game_start_time)
        st.write(f"Time: {elapsed_time // 60}m {elapsed_time % 60}s")
