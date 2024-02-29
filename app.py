import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from word_generator import WordGenerator
from hangman_env import HangmanGame
import random

# External stylesheets for additional styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'styles.css']

app = dash.Dash(__name__, title="Hangman Game", external_stylesheets=external_stylesheets)

# Initialize the game state
game_state = {
    "word_to_guess": None,
    "guessed_word": None
}

# Initial layout for the home page
home_layout = html.Div([
    html.Div(className='header-bar', children=[html.H1("Hangman Game")]),

    html.Div(id='hangman-art', children=[
        html.Pre("""
  -----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
-------
        """)
    ]),

    html.Button('Start Game', id='start-button', n_clicks=0),
])

# Layout for the game page
game_layout = html.Div([
    html.Div(className='header-bar', children=[html.H1("Hangman Game")]),
    
    # Game environment
    html.Div(id='game-environment', children=[
        html.Div(id='word-display'),
        dcc.Input(id='guess-input', type='text', placeholder='Enter your guess'),
        html.Div(id='game-message'),
        html.Button('Guess', id='guess-button', n_clicks=0),
    ])
])



# App layout
app.layout = html.Div([
    html.Div(id='page-content', children=home_layout),
    dcc.Store(id='game-state-store', data={'in_game_mode': False})
])

# Callback to switch between home layout and game layout
@app.callback(
    [Output('page-content', 'children'),
     Output('game-state-store', 'data')],
    [Input('start-button', 'n_clicks')],
    [State('guess-input', 'value')]
)
def display_page(n_clicks, guess_input_value):
    if n_clicks > 0:
        # Reset game state
        game_state["word_to_guess"] = random.choice(WordGenerator.generate_word_list())
        game_state["guessed_word"] = ['_'] * len(game_state["word_to_guess"])
        return game_layout, {'in_game_mode': True}
    else:
        return home_layout, {'in_game_mode': False}

    
# Callback to handle game logic
@app.callback(
    [Output('game-environment', 'children'),
     Output('game-message', 'children')],
    [Input('guess-button', 'n_clicks')],
    [Input('guess-input', 'value')],
    [State('game-state-store', 'data')]
)
def hangman_game(n_clicks, guessed_letter, game_state_data):
    if not game_state_data['in_game_mode']:
        return dash.no_update

    if n_clicks == 0:
        return [
            html.Div(id='word-display', children=['_ ' * len(game_state["word_to_guess"])]),
            html.Div(id='game-message', children=[""])
        ]

    # Add your game logic here
    # Check if the guessed letter is in the word_to_guess
    if guessed_letter in game_state["word_to_guess"]:
        # Update the guessed_word with the correctly guessed letter
        for i, letter in enumerate(game_state["word_to_guess"]):
            if letter == guessed_letter:
                game_state["guessed_word"][i] = guessed_letter

    # Check if the player has won
    if '_' not in game_state["guessed_word"]:
        game_message = "Congratulations! You've guessed the word."
    else:
        game_message = ""

    return [
        html.Div(id='word-display', children=[' '.join(game_state["guessed_word"])]),
        html.Div(id='game-message', children=[game_message])
    ]


if __name__ == '__main__':
    app.run_server(debug=True)

