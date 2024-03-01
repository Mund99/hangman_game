import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
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
    dcc.Location(id='url', refresh=False),
    dcc.Link(
        html.Button('Start Game', id='start-button', n_clicks=0), 
        href='/gameplay',
        className='start-button-link'
        )
])