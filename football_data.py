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
        html.Div([
            html.Div([
                # single team controls div
                html.H2('Single Team Analysis', style={'font-size':'1.4em'}),
                html.Div([
                    html.H2('Choose team.', style={'font-size':'1.2em'}),
                    dcc.Dropdown(id='team-picker', options=teams, value=teams[0]['value']),
                ]),
                html.Div([
                    html.H2('Choose season.', style={'font-size':'1.2em'}),
                    dcc.Dropdown(id='season-picker', options=seasons, value=seasons[0]['value']),
                ]),
            ], style={'height':'505px', 'borderBottom':'1px solid #E1E1E1'}),
            html.Div([
                # team stats over years controls div
                html.H2('Team Year On Year', style={'font-size':'1.4em'}),
                html.Div([
                    html.H2('Choose team.', style={'font-size':'1.2em'}),
                    dcc.Dropdown(id='team-picker1', options=teams, value=teams[0]['value']),
                ]),
                html.Div([
                    html.H2('Choose season.', style={'font-size':'1.2em'}),
                    dcc.Checklist(id='season-picker1', options=seasons, values=[seasons[-3]['value'], seasons[-2]['value'], seasons[-1]['value']], labelStyle={'margin':'10px 0px', 'display':'block'}, inputStyle={'marginRight':'10px'}), #seasons[0]['value']
                ]),
            ], style={'height':'505px', 'borderBottom':'1px solid #E1E1E1'}),
            html.Div([
                # leage on leage controls div
                html.H2('League On League ', style={'font-size':'1.4em'}),
                html.Div([
                    html.H2('Choose season.', style={'font-size':'1.2em'}),
                    dcc.Dropdown(id='season-picker2', options=seasons, value=seasons[0]['value']),
                ]),
            ], style={'height':'505px', 'borderBottom':'1px solid #E1E1E1'}),
        ], style={'width':'15%', 'borderRight':'1px solid #E1E1E1', 'padding':'0px 20px', 'float':'left', 'display':'inline-block', 'backgroundColor':colours['background_grey']}),
        # single team stats
        html.Div([
            html.H2('Single Team Analysis', style={'font-size':'1.2em'}),
            html.Div([
                dcc.Graph(id='graph'),
            ], style={'width':'60%', 'float':'left', 'display':'inline-block', 'marginBottom':'20px', 'paddingRight':'20px'}),
            html.Div([
                dcc.Graph(id='table'),
            ], style={'width':'35%', 'marginTop':'0px', 'float':'left', 'display':'inline-block'}),
            html.P('',style={'clear':'both'}),
        ], style={'float':'left', 'width':'80%', 'borderBottom':'1px solid #E1E1E1', 'marginLeft':'20px'}),
        # team stats year over year
        html.Div([
            html.H2('Team Year On Year Analysis', style={'font-size':'1.2em'}),
            html.Div([
                dcc.Graph(id='graph1'),
            ], style={'width':'60%', 'float':'left', 'display':'inline-block', 'marginBottom':'20px', 'paddingRight':'20px'}),
            html.Div([
                dcc.Graph(id='table1'),
            ], style={'width':'35%', 'marginTop':'0px', 'float':'left', 'display':'inline-block'}),
        ], style={'float':'left', 'width':'80%', 'borderBottom':'1px solid #E1E1E1', 'marginLeft':'20px'}),
        # league on league stats
        html.Div([
            html.H2('League On League Analysis', style={'font-size':'1.2em'}),
            html.Div([
                dcc.Graph(id='graph2'),
            ], style={'width':'48%', 'float':'left', 'display':'inline-block', 'marginBottom':'20px', 'paddingRight':'20px'}),
            html.Div([
                dcc.Graph(id='graph3'),
            ], style={'width':'48%', 'marginTop':'0px', 'float':'left', 'display':'inline-block'}),
        ], style={'float':'left', 'width':'80%', 'borderBottom':'1px solid #E1E1E1', 'marginLeft':'20px'}),
    ]),
    # footer div
    html.P([], style={'clear':'both'}),
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
            yaxis={'title':'Value [Total For Seaon]'},
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

@app.callback(Output('graph1', 'figure'),
              [Input('team-picker1', 'value'),
               Input('season-picker1', 'values')])
def update_year_graph(chosen_team, chosen_season):
    traces = []
    for season in chosen_season:
        # filter data on given team
        filtered_df_home = df[(df['HomeTeam']== chosen_team) & (df['Season']== season)]
        filtered_df_away = df[(df['AwayTeam']== chosen_team) & (df['Season']== season)]

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

        traces.append(go.Bar(x = ['Points', 'Goals For', 'Goals Against', 'Yellow Cards', 'Red Cards'],
                             y = [sum(points_home + points_away), goals_for_home + goals_for_away, goals_against_home + goals_against_away, yellow_cards_home + yellow_cards_away, red_cards_home + red_cards_away],
                             name = season))

    return {'data' : traces,
            'layout':go.Layout(title= str(chosen_team),
            xaxis={'title':'Statistic', 'type':'category'},
            yaxis={'title':'Value [Total For Season]'},
            barmode='group'),
    }

@app.callback(Output('table1', 'figure'),
              [Input('team-picker1', 'value'),
               Input('season-picker1', 'values')])
def update_year_table(chosen_team, chosen_season):
    traces = []
    header = ['<b>Statistic</b>']
    values = [['<b>Points</b>','<b>Goals For</b>','<b>Goals Against</b>', '<b>Yellow Cards</b>', '<b>Red Cards</b>']]
    for season in chosen_season:
        # filter data on given team
        filtered_df_home = df[(df['HomeTeam']== chosen_team) & (df['Season']== season)]
        filtered_df_away = df[(df['AwayTeam']== chosen_team) & (df['Season']== season)]

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

        header.append('<b>' + season + ' Total</b>')
        header.append('<b>' + season + ' Avg</b>')
        values.append([sum(points_home + points_away),goals_for, goals_against, yellow_cards, red_cards])
        values.append([round(sum(points_home + points_away)/games_played, 2), round(goals_for/games_played, 2), round(goals_against/games_played, 2), round(yellow_cards/games_played, 2), round(red_cards/games_played, 2)])

    trace = go.Table(header=dict(values=header,
                                 line = dict(color=colours['line_colour']),
                                 fill = dict(color=colours['background_grey']),
                                 font=dict(family='Calibri', size=16, color=colours['text_main']),
                                 height = 35),
                     cells=dict(values=values,
                                line = dict(color=colours['line_colour']),
                                font=dict(family='Calibri', size=16, color=colours['text_main']),
                                height = 35))

    return {'data' : [trace],
            'layout':go.Layout(title= str(chosen_team),width=650, height=470)
    }

@app.callback(Output('graph2', 'figure'),
              [Input('season-picker2', 'value')])
def update_league_graph(chosen_season):
    leagues = []
    for league in df['League'].unique():
        leagues.append(league)

    filtered_df = df[df['Season']== chosen_season]
    traces = []

    for league in leagues:
        filtered_df_league = filtered_df[filtered_df['League']== league]
        games_played = filtered_df_league['HomeTeam'].count()

        goals_for = (sum(filtered_df_league['FTHG']) + sum(filtered_df_league['FTAG']) / games_played)
        goals_against = (sum(filtered_df_league['FTAG']) + sum(filtered_df_league['FTHG']) / games_played)
        yellow_cards = (sum(filtered_df_league['HY']) + sum(filtered_df_league['AY']) / games_played)
        red_cards = (sum(filtered_df_league['HR']) + sum(filtered_df_league['AR']) / games_played)

        points_home = []
        for game in filtered_df_league['FTR']:
            if game == 'H':
                points_home.append(3)
            elif game == 'D':
                points_home.append(1)
        points_away = []
        for game in filtered_df_league['FTR']:
            if game == 'A':
                points_away.append(3)
            elif game == 'D':
                points_away.append(1)

        traces.append(go.Bar(x = ['Points', 'Goals For', 'Goals Against', 'Yellow Cards', 'Red Cards'],
                             y = [(sum(points_home + points_away)), goals_for, goals_against, yellow_cards, red_cards],
                             name = league))

    return {'data' : traces,
            'layout':go.Layout(title= str(chosen_season),
            xaxis={'title':'Statistic', 'type':'category'},
            yaxis={'title':'Value [Total For Season]'},
            barmode='group'),
    }

@app.callback(Output('graph3', 'figure'),
              [Input('season-picker2', 'value')])
def update_league_graph(chosen_season):
    leagues = []
    for league in df['League'].unique():
        leagues.append(league)

    filtered_df = df[df['Season']== chosen_season]
    traces = []

    for league in leagues:
        filtered_df_league = filtered_df[filtered_df['League']== league]
        games_played = filtered_df_league['HomeTeam'].count()

        goals_for = (sum(filtered_df_league['FTHG']) + sum(filtered_df_league['FTAG']) / games_played) / games_played
        goals_against = (sum(filtered_df_league['FTAG']) + sum(filtered_df_league['FTHG']) / games_played) / games_played
        yellow_cards = (sum(filtered_df_league['HY']) + sum(filtered_df_league['AY']) / games_played) / games_played
        red_cards = (sum(filtered_df_league['HR']) + sum(filtered_df_league['AR']) / games_played) / games_played

        points_home = []
        for game in filtered_df_league['FTR']:
            if game == 'H':
                points_home.append(3)
            elif game == 'D':
                points_home.append(1)
        points_away = []
        for game in filtered_df_league['FTR']:
            if game == 'A':
                points_away.append(3)
            elif game == 'D':
                points_away.append(1)

        traces.append(go.Bar(x = ['Points', 'Goals For', 'Goals Against', 'Yellow Cards', 'Red Cards'],
                             y = [(sum(points_home + points_away)) / games_played, goals_for, goals_against, yellow_cards, red_cards],
                             name = league))

    return {'data' : traces,
            'layout':go.Layout(title= str(chosen_season),
            xaxis={'title':'Statistic', 'type':'category'},
            yaxis={'title':'Value [Average Per Game]'},
            barmode='group'),
    }



if __name__ == '__main__':
    app.run_server(debug=True)
