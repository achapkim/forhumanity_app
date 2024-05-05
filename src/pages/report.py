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
            html.H1("Report", style = {'textAlign': 'center',
            'marginTop': '1rem',
            'marginBottom': '1rem'}
            ),
            html.Iframe(src=app.get_asset_url('report.pdf'),
                                            style= {"position":"absolute",
                                                    "width": '100%',
                                                    "height":'100%',
                                                    'align-items':'center',
                                                    'border':'none'
                                            })
    ])

