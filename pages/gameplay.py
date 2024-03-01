import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import random

dash.register_page(__name__, 
                   title='Hangman Game',
                   path='/gameplay',
                   )

# Read words from 'assets/wordbank.txt'
with open('assets/wordbank.txt', 'r') as file:
    word_list = file.read().splitlines()

# Get a random word for the game
random_word = random.choice(word_list)

# Convert the word to a list of characters
word_characters = list(random_word.upper())

# Create a set to keep track of guessed letters
guessed_letters = set()

# Set the maximum number of incorrect guesses
max_attempts = 6

# Initialize the current state of the game
current_state = {
    'word': word_characters,
    'guessed_word': ['_ ' if char.isalpha() else char for char in word_characters],
    'incorrect_attempts': 0,
    'game_over': False,
    'game_won': False
}

# Hangman images
hangman_images = [
"""
  -----
  |   |
      |
      |
      |
      |
-------
""",
"""
  -----
  |   |
  O   |
      |
      |
      |
-------
""",
"""
  -----
  |   |
  O   |
  |   |
      |
      |
-------
""",
"""
  -----
  |   |
  O   |
 /|   |
      |
      |
-------
""",
"""
  -----
  |   |
  O   |
 /|\\  |
      |
      |
-------
""",
"""
  -----
  |   |
  O   |
 /|\\  |
 /    |
      |
-------
""",
"""
  -----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
-------
"""
]


# Define the layout for the Hangman environment
layout = html.Div([
    html.Div(className='header-bar', children=[html.H1("Hangman Game")]),
    html.Div(id='game-environment', children=[
        html.Pre(id='hangman-image', children=[hangman_images[0]]),
        html.Div(id='game-message'),
        html.Div(id='error-message', style={'color': 'red'}),
        html.Div(id='word-display', children=' '.join(current_state['guessed_word'])),
        dcc.Input(id='guess-input', type='text', placeholder='Enter your guess'),
        html.Button('Guess', id='guess-button', n_clicks=0),
        html.Button('Restart Game', id='restart-button', n_clicks=0),
        dcc.Link(html.Button('Back to Home'), href='/'),  # Link to the home page
    ]),
])


# Define callback to update the game state based on the user's guess
@callback(
    [Output('word-display', 'children'),
     Output('game-message', 'children'),
     Output('error-message', 'children'),
     Output('guess-input', 'value'),
     Output('guess-button', 'disabled'),
     Output('guess-button', 'n_clicks'),
     Output('hangman-image', 'children')],
    [Input('guess-button', 'n_clicks'),
     Input('restart-button', 'n_clicks')],
    [State('guess-input', 'value')]
)
def update_game_state(guess_n_clicks, restart_n_clicks, guess, current_state=current_state):
    ctx = dash.callback_context

    if not ctx.triggered_id:
        raise PreventUpdate

    error_message = ''
    if not current_state['game_over']:
        # Process the user's guess
        if ctx.triggered_id == 'guess-button.n_clicks':
            guess = guess.upper()
            if len(guess) == 1 and guess.isalpha():
                if guess not in guessed_letters:
                    guessed_letters.add(guess)
                    if guess not in current_state['word']:
                        current_state['incorrect_attempts'] += 1

                    # Update the guessed word
                    current_state['guessed_word'] = [
                        letter if letter == guess or letter in guessed_letters else '_'
                        for letter in current_state['word']
                    ]

                    # Check if the game is won
                    if '_' not in current_state['guessed_word']:
                        current_state['game_over'] = True
                        current_state['game_won'] = True

                    # Check if the game is lost
                    elif current_state['incorrect_attempts'] >= max_attempts:
                        current_state['game_over'] = True
                else:
                    error_message = 'You already guessed that letter!'
            elif len(guess) != 1:
                error_message = 'Please enter only one letter.'
            elif not guess.isalpha():
                error_message = 'Please enter a valid alphabetical letter.'

        # Display the updated game state
        return (
            ' '.join(current_state['guessed_word']),
            get_game_message(current_state),
            error_message,
            '',
            current_state['game_over'],
            guess_n_clicks + 1,
            [html.Pre(hangman_images[current_state['incorrect_attempts']])]
        )
    elif ctx.triggered_id == 'restart-button.n_clicks':
        # Restart the game
        return initialize_game()

    raise PreventUpdate


# Function to initialize the game state
def initialize_game():
    new_random_word = random.choice(word_list)
    new_word_characters = list(new_random_word.upper())

    return (
        ' '.join(['_ ' if char.isalpha() else char for char in new_word_characters]),
        '',
        '',
        '',
        False,
        0,
        [html.Pre(hangman_images[0])],
    )

# Function to generate game messages based on the current state
def get_game_message(state):
    if state['game_won']:
        return "Congratulations! You guessed the word."
    elif state['game_over']:
        return f"Game over. The word was '{''.join(state['word'])}'. Try again!"
    else:
        return f"Incorrect attempts: {state['incorrect_attempts']}/{max_attempts}"
