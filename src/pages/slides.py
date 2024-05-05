from dash import html
import pandas as pd
import pathlib
from utils import Header

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

def create_layout(app):
    return html.Div([
            Header(app), 
            html.Br([]),
            html.H1("Slides", style = {'textAlign': 'center',
            'marginTop': '1rem',
            'marginBottom': '1rem'}
            ),
            html.Iframe(src=('https://docs.google.com/presentation/d/e/2PACX-1vQkdiGq2wzxDxNHqYNfII9LPlNEEqdtvUoS4bweyNmw2oocTn5LWIbpnrcq5mLPNw/embed?start=false&loop=false&delayms=3000'),
                            style= {"display": "block",
                            "width": "100%",  # Updated to take full width
                            "height": "100vh",  # Updated to take full vertical space
                            "allowfullscreen": "true", 
                            "marginLeft": "auto",
                            "marginRight": "auto"})
    ])
