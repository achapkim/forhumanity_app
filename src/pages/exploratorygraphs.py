from dash import dcc, html
import pandas as pd
import pathlib
import ast
import dash
import datetime
import seaborn as sns
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from utils import Header
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("incidents.csv"))
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

df.set_index('date', inplace=True)

# Resample the data to get the count of incidents 
g1 = df.resample('M').size()

df['Alleged deployer of AI system'] = df['Alleged deployer of AI system'].apply(lambda x: ', '.join(eval(x)))
df['Alleged developer of AI system'] = df['Alleged developer of AI system'].apply(lambda x: ', '.join(eval(x)))
df['Alleged harmed or nearly harmed parties'] = df['Alleged harmed or nearly harmed parties'].apply(lambda x: ', '.join(eval(x)))

df['Match'] = df['Alleged deployer of AI system'] == df['Alleged developer of AI system']

g2 = df['Match'].value_counts()


# Group by year and 'Alleged harmed or nearly harmed parties' column and count occurrences
trends_df = df.groupby([df['year'], 'Alleged harmed or nearly harmed parties']).size().reset_index(name='Count')

# Group the data by year and 'Alleged deployer of AI system' column and count occurrences
grouped_by_year2 = df.groupby(['year', 'Alleged developer of AI system']).size().reset_index(name='Count')

# Filter the DataFrame to include only rows where the count is over 2
filtered_grouped_by_year2 = grouped_by_year2[grouped_by_year2['Count'] > 2]
def g4():
    fig = go.Figure()
    for category in filtered_grouped_by_year2['Alleged developer of AI system'].unique():
        category_data = filtered_grouped_by_year2[filtered_grouped_by_year2['Alleged developer of AI system'] == category]
        fig.add_traces(go.Scatter(x=category_data['year'], y = category_data['Count'], name=category.capitalize()))
        
    fig.update_layout(
                xaxis_title_text='Year', 
                yaxis_title_text='Count')
    return fig
d5 = pd.read_csv(DATA_PATH.joinpath("mindata.csv"))
d5 = d5[d5.columns[1:]]
d5['date_published'] = pd.to_datetime(d5['date_published'], format='%Y-%m-%dT%H:%M:%S.%fZ')
d5['year'] = d5['date_published'].dt.year
d5['month'] = d5['date_published'].dt.month
d5.dropna(subset=['title'], inplace=True) # dropping values with literally no information

def create_count(data):
    timey = data.groupby(['year', 'month']).size()
    timey = timey.reset_index(level=[0, 1])
    # timey['date'] = timey['year'].astype(str) + '-' + timey['month'].astype(str)
    timey['date'] = pd.to_datetime(timey['year'].astype(str) + '-' + timey['month'].astype(str), format='%Y-%m').dt.strftime('%Y-%m')
    timey.columns = [['year', 'month', 'count', 'date']]
    
    # it won't let me use multiindex dataframes so this is necessary
    time = pd.DataFrame()
    time['day'] = timey['date']
    time['num'] = timey['count']
    time = time[:-1] # the last datapoint is false and skews everything
    return time

time = create_count(d5)

def query_entities(data, entity): 
    filtered_data = data[data['title'].str.lower().str.contains(entity.lower())]
    time = create_count(filtered_data)
    return time
    
def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def create_layout(app):
    return html.Div(children=[
        Header(app),
        html.Br([]),
        html.H1("Exploratory Graphs", style = {'textAlign': 'center',
            'marginTop': '1rem',
            'marginBottom': '1rem'}
        ),

        # Graph 1 - Full width
        html.Div([
            html.H2('From Year to Year: The Flow of Incident Reports'),
            dcc.Graph(
                id='graph1',
                figure={
                    'data': [go.Scatter(x=g1.index, y=g1.values, mode='lines+markers', marker=dict(
            color='dodgerblue'))],
                    'layout': go.Layout(
                        xaxis_title_text='Date',
                        yaxis_title_text='Number of Incidents',
                        autosize=True,  # This can help with responsiveness
                        margin=dict(l=40, r=40, t=40, b=40)  # Adjust margins as needed
                    )
                }
            ),
            html.P("The data revealed a notable trend: the emergence of major new technologies or platforms typically results in a surge in incident reports. These spikes in incidents consistently coincide with periods of increased adoption of new technology. For instance, as depicted in the graph above, the uptick in incidents observed in late-2022 correlates with the public introduction of ChatGPT.", id = 'graph1-desc'),
        ]),  # Ensure div is full width

        # Graphs 2 and 3 - Side by side
        html.Div([
            # Graph 2
            html.Div([
                html.H2('Matching Alleged Deployer with Alleged Developer of AI System'),
                dcc.Graph(
                    id='graph2',
                    figure = {'data': [go.Bar(x=['Match', 'Mismatch'], y=g2.values, marker_color=['hotpink', 'dodgerblue'])],
                    'layout': go.Layout(xaxis_title_text='Match', yaxis_title_text='Count')}
                ),
                html.P("There are quite a bit of organizations that both develop and deploy their technologies, but there are also quite a bit of organizations that do not develop the technologies they deploy.", id = 'graph2-desc'),
            ]),

            # Graph 3
            html.Div([
                html.H2("Top 10 Frequencies of Developer/Deployer"),
                dcc.Graph(
                    id='aideploy'),
                    dcc.RadioItems(
                    id='graph-type',
                    options=[
                        {'label': 'Deployer', 'value': 'deployer'},
                        {'label': 'Developer', 'value': 'developer'}
                    ],
                    value='deployer',
                    labelStyle={'display': 'block'}
                ),
                html.P("These plots display the top 10 developers (organizations who have made the technology) or deployers (organizations who have used the technology). Tech companies are one of the largest deployers and developers of AI systems. However, it seems like a good majority of AI systems have been developed by unknown organizations (not mentioned in report).", id = 'graph3-desc'),
            ]),
        ]),

        # Graph 4 - Full width
        html.Div([
            html.H2('Trends in Alleged Developer of AI System (Count > 2) Over the Years'),
            dcc.Graph(
                id='graph4',
                figure=g4() 
            ),
            html.P("This graph displays the systems created by different organizations over the past few years. One thing to note is the explosion of AI systems by OpenAI in the year 2023. We are confident that in 2024, many organizations present will release products that match OpenAI.", id = 'graph4-desc'),
        ]),  # Ensure div is full width

        # Graph 5 - Full width
        html.Div([
            html.H2('Temporal Mapping of Incidents'),
            dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=time['day'].min(),
                        end_date=time['day'].max(),
                        style = {'display':'block', 'margin-left':'auto', 'margin-right':'auto', 'text-align':'center','border':'none', 'border-radius':'4px'},
                        display_format='YYYY-MM-DD',
                        initial_visible_month=datetime.date.today().strftime('%Y-%m'),
            ),
            dcc.Graph(
                id='graph5'
            ),
            html.H4('Organization Query', style = {'text-align':'justify'}),
            dcc.Input(
                        id='search-bar',
                        type='text',
                        placeholder='Search...',
                        style={'text-align':'center', 'margin': 'auto',  'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block', 'border-radius': '4px', 'border-color': '#232d4b'},
                    ),

            html.P("This graph displays the number of reports per organization. You can fine tune the date or search an organization. ", id = 'graph5-desc'),
        ]),  # Ensure div is full width
    ], id='graphs-page')

       
def exp_callbacks(app):
    @app.callback(
        Output("aideploy", "figure"),
        [Input('graph-type', 'value')]
   
    )
    # Top 10 counts 
    def figure_10_cat(graph_type):
        if graph_type == 'developer':
            top_10_categories_dev = df['Alleged developer of AI system'].value_counts().nlargest(10)
            
            # Generate the color palette
            colors = sns.light_palette("hotpink", n_colors=len(top_10_categories_dev), reverse=True)

            # Convert RGB colors to hex format
            hex_colors = [rgb2hex(int(c[0]*255), int(c[1]*255),int(c[2]*255)) for c in colors]

            histogram = px.histogram(top_10_categories_dev, x = top_10_categories_dev.values, y = top_10_categories_dev.index.str.capitalize(),color = top_10_categories_dev.index.str.capitalize(), color_discrete_sequence = hex_colors)
            
            figure = go.Figure(data=histogram)
            
            figure.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title_text='Frequency', 
                yaxis_title_text='Alleged Developer of AI System')


            return figure
            
        elif graph_type == 'deployer':
            top_10_categories_dev = df['Alleged deployer of AI system'].value_counts().nlargest(10)
            
            # Generate the color palette
            colors = sns.light_palette("dodgerblue", n_colors=len(top_10_categories_dev), reverse=True)

            # Convert RGB colors to hex format
            hex_colors = [rgb2hex(int(c[0]*255), int(c[1]*255),int(c[2]*255)) for c in colors]
            
            histogram = px.histogram(top_10_categories_dev, x = top_10_categories_dev.values, y = top_10_categories_dev.index.str.capitalize(), color = top_10_categories_dev.index.str.capitalize(), color_discrete_sequence = hex_colors)

            figure = go.Figure(data=histogram)

            figure.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title_text='Frequency', 
                yaxis_title_text='Alleged Deployer of AI System')
            
            return figure

    @app.callback(
        Output('graph5', 'figure'),
        [Input('search-bar', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),]
    )
    
    def update_chart(search, start_date, end_date):
        if search:
            time = query_entities(d5, search)
        else:
            time = create_count(d5)
        filtered_data = time.query("day >= @start_date and day <= @end_date")
        fig = px.bar(filtered_data, x='day', y='num')
        fig.update_layout(xaxis_title='Date', yaxis_title='Count')
        return fig

