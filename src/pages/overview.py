import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, get_footer

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

def create_layout(app):
    return html.Div(
        [
            Header(app), 
                html.Div(className='content', children=[
        html.Div(className='row', children=[
            html.Div(className='column', children=[
                html.H2('Introduction'),
                html.P("""
As artificial intelligence increasingly permeates daily life, the 'ForHumanity Auditing AI System' utilizes data science to audit AI systems, mitigating risk and enhancing transparency for responsible use. Our goal was to address challenges posed by harm and incidents in artificial intelligence by conducting a thorough analysis of AI-related data. Leveraging data science techniques, we uncovered correlations and directional trends in harm and incidents, delivering meaningful insights to ForHumanity.

The AI Incident Database is a publicly accessible repository that collects and categorizes reports of incidents involving artificial intelligence systems. These incidents generally include cases where AI technologies have functioned in unintended or harmful ways. The purpose of the database is to document these occurrences to provide insight into potential risks, promote transparency, and inform better practices for AI development and deployment.""")
            ]),
            html.Div(className='column', children=[
                html.H2('Topic Modeling'),
                html.Img(src=app.get_asset_url('topic.png'), className = 'image1'),
                html.P("""
                The graphic above is a snapshot of 30 words within incident descriptions that were highly correlated with one another according to a topic model built with Latent Dirichlet Allocation. LDA helps uncover relationships between words that are not immediately obvious and help grouped incidents in a large dataset into themes. Based on the terms above, there is a relation between harmed parties and generative technology malfunction.
                """)
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='column', children=[
                html.H2('Methods'),
                html.P("""
                To extract insights from the AI Incident Database, we utilized several data analysis techniques. Topic Modeling helped identify common themes within the incident reports, such as issues related to privacy, ethical abuses, or technological failures. This method analyzes patterns of words to uncover the dominant topics discussed across various incidents.

Additionally, we employed Word Embedding and Clustering to deepen our analysis. Word Embedding converts text into numerical data, revealing semantic relationships between words. This technique helped us understand contextual similarities between different incidents. Clustering organized these incidents into distinct groups based on their characteristics and severity. This structured approach not only clarified the types of problems encountered but also assisted in formulating targeted responses to different categories of AI-related issues. 

We also did a geopolitical analysis to categorize incidents report by regions focusing on distinguishing between United States and Non- US incidents. We used location extraction from SpaCy library to identify geopolitical entities from the text data. We also used geocoding using Nomination geocoder to convert the textual geographical names into address information and some region classification to determine its relevance to the United States. 

To further augment our analytical process, we developed an interactive dashboard. This centralized platform features dynamic visualization and interactive elements to showcase our work and exploratory data analysis comprehensively. 

                """) 
            ]),
            html.Div(className='column', children=[
                html.H2('Analysis'),
                html.P("""
The Artificial Intelligence Incident Database (AIID) consists of a list of reports on situations when AI went awry. Each data entry contains the author of the report, the date of publication, the title of the article, the text of the article, and numerous other data features pertaining to the article. A thorough parsing of this data allowed for an analysis that highlights periods of increased incidents. By employing natural language processing techniques to analyze the text of these reports, we can identify frequently occurring words and phrases, uncovering common themes and specific technical or ethical issues being reported. This analysis helps in understanding the interactions within sectors that heavily employ AI and tracks the evolution of AI reliability and the effectiveness of measures implemented to mitigate these risks.
                """)   
            ]),
            html.Div(className='column', children=[
                html.H2('Results'),
                html.Ol([
                    html.Li('In a limited manner, we can predict future spikes in AI incidents. Common patterns can be uncovered within the data that can provide prescient insight into future spikes in AI incidents. Periods of widespread adoption and consumption of AI tools, major social upheavals (such as the COVID-19 pandemic), and introduction of major technological advancements are all indications of future reporting spikes.'),
                    html.Li('The United States is highly over-represented in terms of AI Incident reporting. The conclusion reached regarding the AIID is that there were over 4x reports from the United States than there were from outside countries. There is potential for expanding awareness and increasing international engagement to better capture global AI incidents.'),
                    html.Li('From a sector perspective, It’s difficult to conclusively answer whether certain sector are “over-” or “under-represented”, given that the database provided to us is relatively small. It’s intuitively obvious that the tech industry is highly represented in the database, and other prominent sectors include: the education sector, law enforcement, media services, etc.'),
                    html.Li('Performing Named-entity recognition (NER) shows that there is a strong correlation between the media attention devoted to that of a certain corporation and the number of incidents reported regarding said entity. An example of this would be the rapid media attention towards OpenAI leading to a spike in AI incidents reported.'),
                    html.Li('These findings show that there is a pressing need for a comprehensive regulatory frameworks that prioritize ethical considerations, transparency, and accountability in AI development and deployment.')
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='column', children=[
                html.H2('Location Analysis'),
                html.Img(src=app.get_asset_url('ner.png'), className = 'image2'),
                html.P("""
The AI Incident Database is predominantly used by users in the United States, with 488 reports compared to 113 from outside the US. Additionally, 52 reports involve US-based companies. This usage pattern suggests a US-centric focus, reflecting the company's stronger presence in the United States. 
""")  # Location Analysis content goes here
            ]),
            html.Div(className='column', children=[
                html.H2('Insights'),
                html.Strong('The analysis revealed key trends:'),
    html.Ul([
        html.Li('Certain companies frequently coincide with increased incident reports, suggesting a need for closer scrutiny of their product deployment practices.'),
        html.Li('Commonly used terms and phrases across reports often relate to misidentification and bias, particularly within facial recognition and surveillance applications.'),
        html.Li('The rapid integration of AI technologies, such as ChatGPT, aligns closely with a rise in reported incidents, minimizing the challenges of technological adoption without oversight.'),
    ]),
    html.Strong('Challenges identified include:'),
    html.Ul([
        html.Li('The misuse of AI in surveillance and public decision-making, which can amplify existing societal biases.'),
        html.Li('The spread of misinformation by AI systems, particularly in sensitive areas like politics, which poses significant risks to democratic integrity.'),
        html.Li('The exposure of minors to inappropriate content via AI-driven platforms, highlighting critical areas for stricter regulation and oversight.'),
    ]),
                ]),
            ]),
        ])
    ]),
get_footer(app)], id = 'page1')