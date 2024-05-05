import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    return html.Div(
        className='header',
        children=[
            html.Div(
                className='header-title',
                children=[
                    html.H1('ForHumanity Auditing AI System', className='title'),
                    html.H2('Strategic Oversight in Artificial Intelligence', className='subtitle'),
                    html.P('Jacqueline Fraley, Patrick Dunnington, Andrew Chaphiv, Ian Yung', className='team')
                ]
            ),
            html.A(
            html.Div(
                className='header-logo',
                children=[
                    html.Img(
                    src=app.get_asset_url("uvalogo.png"),
                    className="logo")# Replace with the path to your UVA logo image
                ]
            ), href = "https://datascience.virginia.edu/")
        ]
    )


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/dash_app/overview",
                className="tab first",
            ),
            dcc.Link(
                "Report",
                href="/dash_app/report",
                className="tab",
            ),
            dcc.Link(
                "Slides",
                href="/dash_app/slides",
                className="tab",
            ),
            dcc.Link(
                "Exploratory Graphs", href="/dash_app/exp-graph", className="tab"
            ),
            dcc.Link(
                "Word Embeddings",
                href="/dash_app/word-embeddings",
                className="tab",
            ),
            dcc.Link(
                "Topic Modelling",
                href="/dash_app/topic-model",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu

def get_footer(app): 
    return html.Div(
        className = "footer",
        children=[
            html.A(
            html.Div(
                className='footer-logo1',
                children=[
                    html.Img(
                    src=app.get_asset_url("AID_logo.png"),
                    className="logo")# Replace with the path to your UVA logo image
                ]
            ), href = "https://incidentdatabase.ai/"),
            
            html.A(
            html.Div(
                className='footer-logo2',
                children=[
                    html.Img(
                    src=app.get_asset_url("forhumanity_logo.png"),
                    className="logo")# Replace with the path to your UVA logo image
                ]
            ), href = "https://forhumanity.center/")
        ]
    )