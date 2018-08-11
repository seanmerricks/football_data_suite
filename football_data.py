import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from dash.dependencies import Input, Output, State

current_year = datetime.now().year

# data import and processing
xls = pd.ExcelFile('football_data.xlsx')
df = xls.parse('Data')
df.fillna(value=0, inplace=True)

# define teams and seasons in data
teams = []
for team in sorted(df['HomeTeam'].unique()):
    teams.append({'label' : team, 'value' : team})

seasons = []
for season in sorted(df['Season'].unique()):
    seasons.append({'label' : season, 'value' : season})

leagues = []
for league in (df['League'].unique()):
    leagues.append({'label' : league, 'value' : league})


# initialise app
app = dash.Dash()
app.title='Football Data Suite'

# normalisation css
my_css_url = "https://necolas.github.io/normalize.css/8.0.0/normalize.css"
app.css.append_css({
    "external_url": my_css_url
})

colours = {'text_main':'#565656', 'background_grey':'#FBFBFB', 'background_white':'#FFFFFF', 'line_colour':'#E1E1E1'}
tab_style = {'backgroundColor':colours['background_white']}

app.layout = html.Div([
    html.Div([
        html.H1('Football Data Suite', style={'color':colours['text_main'], 'padding':'0px 20px'}),
        html.Hr(style={'margin':0, 'padding':0, 'border':'0', 'backgroundColor':colours['line_colour'], 'height':'1px'}),
    ], style={'backgroundColor':colours['background_white']}),
    html.Div([
        # controls div
        html.Div([
            html.Div([
                html.H2('Choose team.', style={}),
                dcc.Dropdown(id='team-picker', options=teams, value=''), #value=teams[0]['value']
            ]),
            html.Div([
                html.H2('Choose season.', style={}),
                dcc.Dropdown(id='season-picker', options=seasons, value=''), #seasons[0]['value']
            ]),
        ], style={'width':'15%', 'borderRight':'1px solid #E1E1E1', 'padding':'0px 20px', 'float':'left', 'display':'inline-block', 'backgroundColor':colours['background_grey']}),
        # data and graphs
        html.Div([
            html.Div([
                dcc.Graph(id='graph'),
            ], style={'width':'60%', 'borderRight':'1px solid #E1E1E1', 'float':'left', 'display':'inline-block'}),
            html.Div([
                dcc.Graph(id='table'),
            ], style={'width':'35%', 'marginTop':'0px', 'float':'left', 'display':'inline-block'}),
            html.P('',style={'clear':'both'}),
        ], style={'float':'left', 'width':'80%'}),
        html.P('',style={'clear':'both'})
    ]),
    # footer div
    html.Div([
        html.P('Sean Merricks | ' + str(current_year), style={'margin':'0px'}),
        dcc.Markdown('''Data provided by [http://www.football-data.co.uk](http://www.football-data.co.uk). ''')
    ], style={'text-align':'center', 'font-size':'0.8em','paddingBottom':'10px', 'marginTop':'20px'})
], style={'font-family':'calibri', 'color':colours['text_main']})


@app.callback(Output('graph', 'figure'),
              [Input('team-picker', 'value'),
               Input('season-picker', 'value')])
def update_team_graph(chosen_team, chosen_season):
    # filter data on given team
    filtered_df_home = df[(df['HomeTeam']== chosen_team) & (df['Season']== chosen_season)]
    filtered_df_away = df[(df['AwayTeam']== chosen_team) & (df['Season']== chosen_season)]

    games_played = filtered_df_home['HomeTeam'].count() + filtered_df_away['AwayTeam'].count()

    goals_for_home = sum(filtered_df_home['FTHG'])
    goals_against_home = sum(filtered_df_home['FTAG'])
    yellow_cards_home = sum(filtered_df_home['HY'])
    red_cards_home = sum(filtered_df_home['HR'])

    goals_for_away = sum(filtered_df_away['FTAG'])
    goals_against_away = sum(filtered_df_away['FTHG'])
    yellow_cards_away = sum(filtered_df_away['AY'])
    red_cards_away = sum(filtered_df_away['AR'])

    points_home = []
    for game in filtered_df_home['FTR']:
        if game == 'H':
            points_home.append(3)
        elif game == 'D':
            points_home.append(1)
    points_away = []
    for game in filtered_df_away['FTR']:
        if game == 'A':
            points_away.append(3)
        elif game == 'D':
            points_away.append(1)

    trace1 = go.Bar(x = ['Points', 'Goals For', 'Goals Against', 'Yellow Cards', 'Red Cards'], y = [sum(points_home), goals_for_home, goals_against_home, yellow_cards_home, red_cards_home], name = 'Home Games')
    trace2 = go.Bar(x = ['Points', 'Goals For', 'Goals Against', 'Yellow Cards', 'Red Cards'], y = [sum(points_away), goals_for_away, goals_against_away, yellow_cards_away, red_cards_away], name = 'Away Games')

    traces = [trace1, trace2]

    return {'data' : traces,
            'layout':go.Layout(title= str(chosen_team) + ' | ' + chosen_season + ' Season',
            xaxis={'title':'Statistic', 'type':'category'},
            yaxis={'title':'Value'},
            barmode='stack'),
    }

@app.callback(Output('table', 'figure'),
              [Input('team-picker', 'value'),
               Input('season-picker', 'value')])
def update_team_table(chosen_team, chosen_season):
    # filter data on given team
    filtered_df_home = df[(df['HomeTeam']== chosen_team) & (df['Season']== chosen_season)]
    filtered_df_away = df[(df['AwayTeam']== chosen_team) & (df['Season']== chosen_season)]

    games_played = filtered_df_home['HomeTeam'].count() + filtered_df_away['AwayTeam'].count()

    goals_for = sum(filtered_df_home['FTHG']) + sum(filtered_df_away['FTAG'])
    goals_against = sum(filtered_df_home['FTAG']) + sum(filtered_df_away['FTHG'])
    yellow_cards = sum(filtered_df_home['HY']) + sum(filtered_df_away['AY'])
    red_cards = sum(filtered_df_home['HR']) + sum(filtered_df_away['AR'])

    points_home = []
    for game in filtered_df_home['FTR']:
        if game == 'H':
            points_home.append(3)
        elif game == 'D':
            points_home.append(1)
    points_away = []
    for game in filtered_df_away['FTR']:
        if game == 'A':
            points_away.append(3)
        elif game == 'D':
            points_away.append(1)

    trace = go.Table(header=dict(values=['<b>Statistic</b>', '<b>Total For Season</b>', '<b>Average Per Game</b>'],
                                        line = dict(color=colours['line_colour']),
                                        fill = dict(color=colours['background_grey']),
                                        font=dict(family='Calibri', size=16, color=colours['text_main']),
                                        height = 35),
                     cells=dict(values=[['<b>Points</b>','<b>Goals For</b>','<b>Goals Against</b>', '<b>Yellow Cards</b>', '<b>Red Cards</b>'],
                                        [sum(points_home + points_away),goals_for, goals_against, yellow_cards, red_cards],
                                        [round(sum(points_home + points_away)/games_played, 2), round(goals_for/games_played, 2), round(goals_against/games_played, 2), round(yellow_cards/games_played, 2), round(red_cards/games_played, 2)]],
                                        line = dict(color=colours['line_colour']),
                                        font=dict(family='Calibri', size=16, color=colours['text_main']),
                                        height = 35))

    return {'data' : [trace],
            'layout':go.Layout(title= str(chosen_team) + ' | ' + chosen_season + ' Season' + ' | Games Played: ' + str(games_played))
    }

if __name__ == '__main__':
    app.run_server(debug=True)
