# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table

import plotly

from data_analysis import *
import import_utils as iu

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
TOPIC = "#BlackLivesMatter"
df = pd.read_csv('https://raw.githubusercontent.com/pleelapr/twitter-analysis-on-dash/master/data/cleaned_data.csv')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_bar_chart(dataframe, title, id_name):
    return dcc.Graph(
        id=id_name,
        figure={
            'data': [
                {'x': dataframe.iloc[:, 0], 'y': dataframe.iloc[:, 1], 'type': 'bar', 'name': 'SF'}
            ],
            'layout': {
                'title': title
            }
        }
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Twitter Analysis on '+TOPIC),
    html.H2(children="Total Number of Tweets : {}".format(len(df))),
    # html.Div(children='''
    #     Dash: A web application framework for Python.
    # '''),

    # === Tweet Graph and Table
    html.Div([
        html.Label('Rank Tweet By'),
        dcc.Dropdown(
            id='select-rank-tweet-by',
            options=[
                {'label': 'Count of Tweets', 'value': 'text'},
                {'label': 'Number of Retweet', 'value': 'retweet_count'}                
            ],
            value='text'
        ),
        dcc.Graph(id='live-rank-tweet-graph'),
        html.Div(id="live-rank-tweet-table")
    ],style={'width': '48%', 'display': 'inline-block'}),

    # === User Graph and Table
    html.Div([
        html.Label('Rank User By'),
        dcc.Dropdown(
            id='select-rank-user-by',
            options=[
                {'label': 'Number of Tweets by User', 'value': 'user'},
                {'label': 'Number of Followers', 'value': 'user_follower_count'},
                {'label': 'Number of Favorite', 'value': 'user_favorite_count'},
                {'label': 'Number of Retweet from the User', 'value': 'retweet_from_user'}
            ],
            value='user'
        ),
        dcc.Graph(id='live-rank-user-graph'),
        html.Div(id="live-rank-user-table")
    ],style={'width': '48%', 'display': 'inline-block'})
])

# === Tweets Ranking Graph
@app.callback(
    Output('live-rank-tweet-graph', 'figure'),
    [Input('select-rank-tweet-by', 'value')]
)
def update_graph(select_rank_tweet_by):
    if select_rank_tweet_by == 'text':
        output = get_top_count_by(df, 'text')
    elif select_rank_tweet_by == 'retweet_count':
        output = get_rank_col_by_index_col(df, 'retweet_count', 'text', 10)
    return {
        'data': [
                {'x': output.iloc[:, 0], 'y': output.iloc[:, 1], 'type': 'bar', 'name': 'Count'}
            ],
            'layout': {
                'title': 'Tweet Ranking Table'
            }
    }

# === Tweets Ranking Table
@app.callback(
    dash.dependencies.Output("live-rank-tweet-table", "children"),
    [dash.dependencies.Input("select-rank-tweet-by", "value")],
)
def update_output(select_rank_tweet_by):
    if select_rank_tweet_by == 'text':
        output = get_top_count_by(df, 'text')
    elif select_rank_tweet_by == 'retweet_count':
        output = get_rank_col_by_index_col(df, 'retweet_count', 'text', 10)
    return html.Div(
        [
            dash_table.DataTable(
                data=output.to_dict('records'),
                columns=[{"id": x, "name": x} for x in output.columns],
                style_cell={'textAlign': 'left',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'width' : "500px"},
            )
        ]
    )

# === User Ranking Graph
@app.callback(
    Output('live-rank-user-graph', 'figure'),
    [Input('select-rank-user-by', 'value')]
)
def update_graph(select_rank_user_by):
    if select_rank_user_by == 'user':
        output = get_top_count_by(df, 'user')
    elif select_rank_user_by == 'retweet_from_user':
        output = get_top_count_by(df, 'retweet_from_user')
    elif select_rank_user_by == 'user_favorite_count':
        output = get_rank_col_by_index_col(df, 'user_favorite_count', 'user', 10)
    elif select_rank_user_by == 'user_follower_count':
        output = get_rank_col_by_index_col(df, 'user_follower_count', 'user', 10)
    return {
        'data': [
                {'x': output.iloc[:, 0], 'y': output.iloc[:, 1], 'type': 'bar', 'name': 'Count'}
            ],
            'layout': {
                'title': 'User Ranking Table'
            }
    }

# === User Ranking Table
@app.callback(
    dash.dependencies.Output("live-rank-user-table", "children"),
    [dash.dependencies.Input("select-rank-user-by", "value")],
)
def update_output(select_rank_user_by):
    if select_rank_user_by == 'user':
        output = get_top_count_by(df, 'user')
    elif select_rank_user_by == 'retweet_from_user':
        output = get_top_count_by(df, 'retweet_from_user')
    elif select_rank_user_by == 'user_favorite_count':
        output = get_rank_col_by_index_col(df, 'user_favorite_count', 'user', 10)
    elif select_rank_user_by == 'user_follower_count':
        output = get_rank_col_by_index_col(df, 'user_follower_count', 'user', 10)
    return html.Div(
        [
            dash_table.DataTable(
                data=output.to_dict('records'),
                columns=[{"id": x, "name": x} for x in output.columns],
                style_cell={'textAlign': 'left',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'width' : "500px"},
            )
        ]
    )






# def update_text(select_top_count_by):
#     return 'You\'ve entered "{}"'.format(select_top_count_by)

if __name__ == '__main__':
    app.run_server(debug=True)