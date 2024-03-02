import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import random

dash.register_page(__name__, 
                   title='Hangman Game',
                   path='/gameplay',
                   )

# Hangman images
hangman_images = [
"""-----
  |   |
      |
      |
      |
      |
-------""",
"""-----
  |   |
  O   |
      |
      |
      |
-------""",
"""-----
  |   |
  O   |
  |   |
      |
      |
-------""",
"""-----
  |   |
  O   |
 /|   |
      |
      |
-------""",
"""-----
  |   |
  O   |
 /|\\  |
      |
      |
-------""",
"""-----
  |   |
  O   |
 /|\\  |
 /    |
      |
-------""",
"""-----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
-------"""
]

def get_random_word():
    # Read words from 'assets/wordbank.txt'
    with open('assets/wordbank.txt', 'r') as file:
        word_list = file.read().splitlines()

    # Get a random word for the game
    random_word = random.choice(word_list)

    # Convert the word to a list of characters
    random_word = random_word.lower()

    return random_word
random_word = get_random_word()

def initialize_game():
    global random_word, max_lives, guessed_letters, guessing_board, current_state

    # Get a new random word
    random_word = get_random_word()

    # Reset game variables
    max_lives = 6
    guessed_letters = set()
    guessing_board = ['_ ' for _ in range(len(random_word))]
    game_over_won = False

    # Initialize the current state of the game
    current_state = {
        'word': random_word,
        'guessing_board': guessing_board,
        'incorrect_attempts': 0,
        'game_over': game_over_won,
        'game_won': game_over_won,
    }

    return current_state

# Function to generate game messages based on the current state
def get_game_message(state):    
    if state['game_won']:
        return f"Congratulations! You guessed the word."
    elif state['game_over']:
        return f"Game over. The word was '{''.join(state['word'])}'. Try again!"
    else:
        return f"Lives remaining: {max_lives - state['incorrect_attempts']}, Incorrect attempts: {state['incorrect_attempts']}."

def display_guessed_letters(guessed_letters):
    if guessed_letters:
        return f"Guessed letters: {', '.join(sorted(guessed_letters))}"
    else:
        return ''
    
current_state = initialize_game()

# Define the layout for the Hangman environment
layout = html.Div([
    html.Div(className='header-bar', children=[html.H1("Hangman Game")]),
    
    # Game layout container
    html.Div(id='game-container', children=[
        # Left Section
        html.Div(id='left-section', children=[
            html.Div(id='game-message', children=dcc.Markdown(get_game_message(current_state))),
            html.Div(id='guessed-letters'),
            html.Div(id='error-message'),
            html.Div(id='word-display', children=current_state['guessing_board']),
            html.Div(id='guess-container', children=[
                dcc.Input(id='guess-input', type='text', placeholder='Enter your guess'),
                html.Button('Guess', id='guess-button', n_clicks=0),
            ]),
        ]),
        
        # Right Section
        html.Div(id='right-section', children=[
            html.Button('New Game', id='new-game-button', n_clicks=0),
            dcc.Link(html.Button('Home', id='home-button'), href='/', className='button-link'),
            html.Pre(id='hangman-image', children=[hangman_images[0]]),
        ]),
    ]),
    # Use the dcc.Store component to store the current state of the game
    dcc.Store(id='current-state', storage_type='session', data=current_state),
])



# Define callback to update the game state based on the user's guess
@callback(
    [Output('hangman-image', 'children'),
     Output('game-message', 'children'),
     Output('guessed-letters', 'children'),
     Output('error-message', 'children'),
     Output('word-display', 'children'),
     Output('guess-input', 'value'),
     Output('guess-button', 'disabled'),
     Output('guess-button', 'n_clicks'),
     Output('current-state', 'data'), 
     ],
        
    [Input('new-game-button', 'n_clicks'),
     Input('guess-button', 'n_clicks'),
     Input('guess-input', 'n_submit')
     ],
    
    [State('guess-input', 'value'),
     State('current-state', 'data')]
)
def update_game_state(new_game_clicks, guess_button_clicks, enter_press, guess, current_state):    
    ctx = dash.callback_context
    
    if not ctx.triggered_id:
        raise PreventUpdate
    if 'new-game-button' in ctx.triggered_id:
        # Start a new game by calling the initialize_game function
        current_state = initialize_game()
        return (
            [html.Pre(hangman_images[0])],
            get_game_message(current_state), 
            display_guessed_letters(guessed_letters),
            '', 
            current_state['guessing_board'],
            '',
            current_state['game_over'],
            0, 
            current_state,
        )

    error_message = ''

    if not current_state['game_over']:
        # Process the user's guess
        if 'guess-button' in ctx.triggered_id or 'guess-input' in ctx.triggered_id:
            guess = guess.lower()
            if len(guess) == 1 and guess.isalpha():
                if guess not in guessed_letters:
                    guessed_letters.add(guess)
                    if guess not in current_state['word']:
                        current_state['incorrect_attempts'] += 1

                    # Update the guessing board
                    current_state['guessing_board'] = [
                        letter if letter == guess or letter in guessed_letters else '_'
                        for letter in current_state['word']
                    ]

                    # Check if the game is won
                    if '_' not in current_state['guessing_board']:
                        current_state['game_over'] = True
                        current_state['game_won'] = True

                    # Check if the game is lost
                    elif current_state['incorrect_attempts'] >= max_lives:
                        current_state['game_over'] = True
                else:
                    error_message = 'You already guessed that letter!'
            elif len(guess) != 1:
                error_message = 'Please enter only one letter.'
            elif not guess.isalpha():
                error_message = 'Please enter a valid alphabetical letter.'
        
        # Display the updated game state
        return (
            [html.Pre(hangman_images[current_state['incorrect_attempts']])],
            get_game_message(current_state),
            display_guessed_letters(guessed_letters),
            error_message,
            ' '.join(current_state['guessing_board']),
            '',
            current_state['game_over'],
            0,
            current_state,
        )
        
    raise PreventUpdate