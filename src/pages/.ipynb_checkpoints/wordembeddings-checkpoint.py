import pathlib

import numpy as np
from dash import dcc, html
from PIL import Image
from io import BytesIO
from dash.dependencies import Input, Output

from utils import Header 

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import scipy.spatial.distance as spatial_distance

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


vectors = pd.read_csv(DATA_PATH.joinpath("vector_coordinates.csv"),converters={"vector": lambda x: x.strip("[]").replace("\n", "").split(" ")}, index_col = 0)
vectors['vector'] = vectors['vector'].apply(lambda lst: [float(x) for x in lst if x])

with open(PATH.joinpath("../wordembedding_intro.md"), "r") as file:
    demo_intro_md = file.read()

with open(PATH.joinpath("../wordembedding_description.md"), "r") as file:
    demo_description_md = file.read()

# Methods for creating components in the layout code
def Card(children, **kwargs):
    return html.Section(children, className="card-style")


def NamedSlider(name, short, min, max, step, val, marks=None):
    if marks:
        step = None
    else:
        marks = {i: i for i in range(min, max + 1, step)}

    return html.Div(
        style={"margin": "25px 5px 30px 0px"},
        children=[
            f"{name}:",
            html.Div(
                style={"margin-left": "5px"},
                children=[
                    dcc.Slider(
                        id=f"slider-{short}",
                        min=min,
                        max=max,
                        marks=marks,
                        step=step,
                        value=val,
                    )
                ],
            ),
        ],
    )


def NamedInlineRadioItems(name, short, options, val, **kwargs):
    return html.Div(
        id=f"div-{short}",
        style={"display": "inline-block"},
        children=[
            f"{name}:",
            dcc.RadioItems(
                id=f"radio-{short}",
                options=options,
                value=val,
                labelStyle={"display": "inline-block", "margin-right": "7px"},
                style={"display": "inline-block", "margin-left": "7px"},
            ),
        ],
    )


def create_layout(app):
    # Actual layout of the app
    return html.Div(
        children=[
            # Header
            Header(app),
            html.Br([]),
            html.H1("Word Embeddings", style = {'textAlign': 'center',
            'marginTop': '1rem',
            'marginBottom': '1rem'}
            ),
            # Demo Description
            html.Div(
                id="demo-explanation",
                children=[
                    html.Div(
                        id="description-text", children=dcc.Markdown(demo_intro_md), style = {'font-family':'Calibri'}
                    ),
                    html.Div(
                        html.Button(id = "learn-more-button", children=["Learn More"])
                    ),
                ],
            ),
            # Body
            html.Div(
                style={"padding": "10px"},
                children=[
                    html.Div(
                        className="three columns",
                        children=[
                            Card(
                                [
                                    dcc.Dropdown(
                                        id="dropdown-dataset",
                                        searchable=False,
                                        clearable=False,
                                        options=[
                                            {
                                                "label": "Noun",
                                                "value": "NN",
                                            },
                                            {
                                                "label": "Verb",
                                                "value": "VB",
                                            },
                                            {
                                                "label": "Adjective",
                                                "value": "JJ",
                                            },
                                        ],
                                        placeholder="Select a POS Tag",
                                        value="NN",
                                    ),
                                    NamedSlider(
                                        name="Number Of Iterations",
                                        short="iterations",
                                        min=250,
                                        max=1000,
                                        step=None,
                                        val=500,
                                        marks={
                                            i: str(i) for i in [250, 500, 750, 1000]
                                        },
                                    ),
                                    
                                    NamedSlider(
                                        name="Perplexity",
                                        short="perplexity",
                                        min=3,
                                        max=100,
                                        step=None,
                                        val=30,
                                        marks={i: str(i) for i in [5, 10, 30, 50, 100]},
                                    ),
                                  
                                    NamedSlider(
                                        name="Learning Rate",
                                        short="learning-rate",
                                        min=10,
                                        max=200,
                                        step=None,
                                        val=100,
                                        marks={i: str(i) for i in [10, 50, 100, 200]},
                                    ),
                                    html.Div(
                                        id="div-wordemb-controls",
                                        style={"display": "none"},
                                        children=[
                                            NamedInlineRadioItems(
                                                name="Display Mode",
                                                short="wordemb-display-mode",
                                                options=[
                                                    {
                                                        "label": " Regular",
                                                        "value": "regular",
                                                    },
                                                    {
                                                        "label": " Top-100 Neighbors",
                                                        "value": "neighbors",
                                                    },
                                                ],
                                                val="regular",
                                            ),
                                            dcc.Dropdown(
                                                id="dropdown-word-selected",
                                                placeholder="Select word to display its neighbors",
                                                style={"background-color": "#f2f3f4"},
                                            ),
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            dcc.Graph(id="graph-3d-plot-tsne", style={"height": "98vh"})
                        ],
                    ),
                    html.Div(
                        className="three columns",
                        id="euclidean-distance",
                        children=[
                            Card(
                                style={"padding": "5px"},
                                children=[
                                    html.Div(
                                        id="div-plot-click-message",
                                        style={
                                            "text-align": "center",
                                            "margin-bottom": "7px",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(id="div-plot-click-image"),
                                    html.Div(id="div-plot-click-wordemb"),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
    )


def word_callbacks(app):
    # Scatter Plot of the t-SNE datasets
    def generate_figure_word_vec(
        embedding_df, layout, wordemb_display_mode, selected_word, dataset
    ):
        try:
            # Regular displays the full scatter plot with only circles
            if wordemb_display_mode == "regular":
                plot_mode = "markers"

            # Nearest Neighbors displays only the 200 nearest neighbors of the selected_word, in text rather than circles
            elif wordemb_display_mode == "neighbors":
                if not selected_word:
                    return go.Figure()

                plot_mode = "text"

                # Get the nearest neighbors indices using Euclidean distance
                vector = embedding_df[embedding_df['pos_group'] == dataset]['vector']
                selected_vec = embedding_df.loc[selected_word]['vector']

                def compare_pd(v):
                    return spatial_distance.euclidean(v, selected_vec)

                # vector.apply takes compare_pd function as the first argument
                distance_map = vector.apply(compare_pd)
                neighbors_idx = distance_map.sort_values()[:100].index

                # Select those neighbors from the embedding_df
                embedding_df = embedding_df.loc[neighbors_idx]

            scatter = px.scatter(embedding_df[embedding_df['pos_group'] == dataset].reset_index(), 'x', 'y', 
                       text='term_str', 
                       color='max_pos', 
                       hover_name='term_str',          
                       size='size',
                       height=1000)
        
            figure = go.Figure(data=scatter, layout=layout)

            figure.update_traces(
                    mode='markers+text', 
                    textfont=dict(color='black', size=14, family='Arial'),
                    textposition='top center')
            
            return figure
        except KeyError as error:
            print(error)
            raise PreventUpdate

    # Callback function for the learn-more button
    @app.callback(
        [
            Output("description-text", "children"),
            Output("learn-more-button", "children"),
        ],
        [Input("learn-more-button", "n_clicks")],
    )
    def learn_more(n_clicks):
        # If clicked odd times, the instructions will show; else (even times), only the header will show
        if n_clicks is None:
            n_clicks = 0
        if (n_clicks % 2) == 1:
            n_clicks += 1
            return (
                html.Div(
                    style={"padding-right": "15%", 'font-family':'Calibri'},
                    children=[dcc.Markdown(demo_description_md)],
                ),
                "Close",
            )
        else:
            n_clicks += 1
            return (
                html.Div(
                    style={"padding-right": "15%"},
                    children=[dcc.Markdown(demo_intro_md)],
                ),
                "Learn More",
            )

    @app.callback(
        Output("div-wordemb-controls", "style"), [Input("dropdown-dataset", "value")]
    )
    def show_wordemb_controls(dataset):
        return None

    @app.callback(
        Output("dropdown-word-selected", "disabled"),
        [Input("radio-wordemb-display-mode", "value")],
    )
    def disable_word_selection(mode):
        return not mode == "neighbors"

    @app.callback(
        Output("dropdown-word-selected", "options"),
        [Input("dropdown-dataset", "value")],
    )
    def fill_dropdown_word_selection_options(dataset):
        return vectors.index.to_list()

    @app.callback(
        Output("graph-3d-plot-tsne", "figure"),
        [
            Input("dropdown-dataset", "value"),
            Input("slider-iterations", "value"),
            Input("slider-perplexity", "value"),
            Input("slider-learning-rate", "value"),
            Input("dropdown-word-selected", "value"),
            Input("radio-wordemb-display-mode", "value"),
        ],
    )
    def display_3d_scatter_plot(
        dataset, 
        iterations, 
        perplexity,
        learning_rate,
        selected_word,
        wordemb_display_mode,
    ):
            path = f"iterations_{iterations}_perplexity_{perplexity}_learning_rate_{learning_rate}.csv"
            embedding_df = pd.read_csv(DATA_PATH.joinpath(path))

            # Plot layout
            axes = dict(title="", showgrid=True, zeroline=False, showticklabels=False)

            layout = go.Layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(xaxis=axes, yaxis=axes),
            )
           
            figure = generate_figure_word_vec(
                    embedding_df=embedding_df,
                    layout=layout,
                    wordemb_display_mode=wordemb_display_mode,
                    selected_word=selected_word,
                    dataset=dataset,
                )
            if not figure:
                figure = go.Figure()

            return figure

    @app.callback(
        Output("div-plot-click-wordemb", "children"),
        [Input("graph-3d-plot-tsne", "clickData"), Input("dropdown-dataset", "value")],
    )
    def display_click_word_neighbors(clickData, dataset):
        selected_word = clickData["points"][0]["hovertext"]

        try:
            # Get the nearest neighbors indices using Euclidean distance
            vector = vectors['vector']
            selected_vec = vector.loc[selected_word]

            def compare_pd(v):
                return spatial_distance.euclidean(v, selected_vec)

            # vector.apply takes compare_pd function as the first argument
            distance_map = vector.apply(compare_pd)
            nearest_neighbors = distance_map.sort_values()[1:6]

            trace = go.Bar(
                x=nearest_neighbors.values,
                y=nearest_neighbors.index,
                width=0.5,
                orientation="h",
                marker=dict(color="rgb(50, 102, 193)"),
            )

            layout = go.Layout(
                title=f'5 Nearest Neighbors of "{selected_word}"',
                xaxis=dict(title="Euclidean Distance"),
                margin=go.layout.Margin(l=60, r=60, t=35, b=35),
            )

            fig = go.Figure(data=[trace], layout=layout)

            return dcc.Graph(
                id="graph-bar-nearest-neighbors-word",
                figure=fig,
                style={"height": "25vh"},
                config={"displayModeBar": False},
            )
        except KeyError as error:
            raise PreventUpdate
    return None

    @app.callback(
        Output("div-plot-click-message", "children"),
        [Input("graph-3d-plot-tsne", "clickData"), Input("dropdown-dataset", "value")],
    )
    def display_click_message(clickData, dataset):
        if clickData:
            return None
        else:
            return "Click a word on the plot to see its top 5 neighbors."