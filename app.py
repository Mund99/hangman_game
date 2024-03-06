import dash
from dash import html

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', 
    'home.css', 
    'gameplay.css']

# Initialize the Dash app
app = dash.Dash(__name__,
                title='Hangman Game',
                external_stylesheets=external_stylesheets,
                use_pages=True  # Enable the use of dash pages
)

app.layout = html.Div([
    # Include dash.page_container here - this is where the page content will be rendered
    dash.page_container
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)