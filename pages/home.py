import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div(className='header-bar', children=[html.H1("Hangman Game")]),
    
    # Hangman art display using a Pre element
    html.Div(id='hangman-art', children=[
        html.Pre(
"""-----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
-------""")
    ]),
    
    # Location component to keep track of the current URL
    dcc.Location(id='url', refresh=False),
    
    # Link to navigate to the '/gameplay' page when the 'Start Game' button is clicked
    dcc.Link(
        html.Button('Start Game', id='start-button', n_clicks=0), 
        href='/gameplay',
        className='button-link'
        )
])