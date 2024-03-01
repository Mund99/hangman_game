import dash
from dash import dcc, html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'styles.css', 'gameplay.css']

app = dash.Dash(__name__,
                title='Hangman Game',
                external_stylesheets=external_stylesheets,
                use_pages=True
)

# Home page layout
app.layout = html.Div([
    # Include dash.page_container here
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)