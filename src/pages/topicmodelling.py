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
            html.H1("Topic Modelling", style = {'textAlign': 'center',
            'marginTop': '1rem',
            'marginBottom': '1rem'}
            ),
            html.Iframe(src=app.get_asset_url('ldavisual.html'),
                            style= {"display": "block",
                            "width": "100%",  # Updated to take full width
                            "height": "100vh",  # Updated to take full vertical space
                            "allowfullscreen": "true", 
                            "marginLeft": "auto",
                            "marginRight": "auto",
                            "border": "none"})
                                            
    ])

