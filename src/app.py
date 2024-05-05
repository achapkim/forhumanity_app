# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import (
    overview,
    report, 
    slides,
    topicmodelling, 
    exploratorygraphs,
    wordembeddings, 
)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "ForHumanity AI Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash_app/report":
        return report.create_layout(app)
    elif pathname == "/dash_app/slides":
        return slides.create_layout(app)
    elif pathname == "/dash_app/exp-graph":
        return exploratorygraphs.create_layout(app)
    elif pathname == "/dash_app/word-embeddings":
        return wordembeddings.create_layout(app)
    elif pathname == "/dash_app/topic-model":
        return topicmodelling.create_layout(app)
        
    else:
        return overview.create_layout(app)

wordembeddings.word_callbacks(app)
exploratorygraphs.exp_callbacks(app)

if __name__ == "__main__":
    app.run_server(jupyter_mode="tab", dev_tools_ui=True,dev_tools_props_check=False)
