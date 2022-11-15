import dash 
from dash import html, dcc
import mysql.connector as sql
from dash.dependencies import Output, Input, State
import dash_mantine_components as dmc
import pandas as pd 
from dash_iconify import DashIconify

from app import app
from components import curve

class MyDB(object):
    def __init__(self):
        self._dbConnection = sql.connect(
            host='95.216.92.176 ',
            database='TFN_DB',
            user='tfn_db_user',
            password='tfndbuser2020',
            use_pure=True
        )
        #self._db_cur = self._dbConnection.cursor()

    def query(self, query):

        try:
            if self._dbConnection.is_connected():
                return pd.read_sql_query(query, self._dbConnection)
            else:
                self._dbConnection = sql.connect(
                    host='95.216.92.176 ',
                    database='TFN_DB',
                    user='tfn_db_user',
                    password='tfndbuser2020',
                    use_pure=True
                )
                return pd.read_sql_query(query, self._dbConnection)
        except pd.io.sql.DatabaseError as e: 
            print('Something went wrong!!, \n', e)
            return None

    def __del__(self):
        self._dbConnection.close()

mydb = MyDB()

layout = html.Div(children=[
    dmc.Group(direction='column', spacing='md', grow=True, children=[
        dmc.Group(direction='row', spacing='md', children=[
            dcc.Loading(dmc.Select(
                label="Select a Race",
                description="Select one state.",
                id="race_id",
                data=['Governor', 'Senate', 'House'],
                value='Governor',
                style={"width": 200}
            )),
            dcc.Loading(dmc.Select(
                label="Select a State",
                description="Select one state.",
                id="state_id",
                style={"width": 200}, 
                searchable=True
            )),
            dcc.Loading(dmc.Select(
                label="Select a county",
                description="Select one county.",
                id="county_id",
                style={"minWidth": 300}, 
                searchable=True
            )),
            dcc.Loading(dmc.MultiSelect(
                label="Select a candidate",
                description="Select one candidate.",
                id="candidate_id",
                # style={"width": 200}, 
                searchable=True
            )), 
            dmc.Button(
                "Filter",
                id='filter_btn',
                variant="outline",
                leftIcon=[DashIconify(icon="fluent:settings-32-regular")]

            ),
        ], style={"display": 'flex', 'alignItems': 'end'}), 
        dcc.Loading(html.Div(id='timeline_figure'))
    ])
], style={"margin": '40px 20px 40px 20px'})


@app.callback(
    # Output('house_data', 'data'),
    Output('state_id', 'data'),
    Output('state_id', 'value'),
    Input('race_id', 'value')
)
def update_state_dropdown(race_id): 
    global mydb
    data = mydb.query(f'''
        SELECT DISTINCT state_abbr FROM TFN_DB.primary{race_id}Election2022Histo;
    ''')
    return data.state_abbr.tolist(), data.state_abbr.values[0]



@app.callback(
    # Output('house_data', 'data'),
    Output('county_id', 'data'),
    Output('county_id', 'value'),
    Input('state_id', 'value'), 
    State('race_id', 'value')
)
def update_county_dropdown(state_abbr, race_id): 
    data = mydb.query(f'''
        SELECT DISTINCT county 
        FROM TFN_DB.primary{race_id}Election2022Histo
        WHERE state_abbr='{state_abbr}';
    ''')
    return data.county.tolist(), data.county.values[0]


@app.callback(
    # Output('house_data', 'data'),
    Output('candidate_id', 'data'),
    Output('candidate_id', 'value'),
    Input('county_id', 'value'), 
    State('state_id', 'value'), 
    State('race_id', 'value')
)
def update_candidate_dropdown(counties, state_abbr, race_id): 
    
    data = mydb.query(f'''
        SELECT DISTINCT name 
        FROM TFN_DB.primary{race_id}Election2022Histo
        WHERE state_abbr='{state_abbr}' and county = '{counties}';
    ''')
    return data.name.tolist()+['TOTAL VOTES'], data.name.values[:2] # , 'TOTAL BY PARTY'


@app.callback(
    # Output('house_data', 'data')
    Output('timeline_figure', 'children'),
    Input('filter_btn', 'n_clicks'),
    State('candidate_id', 'value'),
    State('county_id', 'value'), 
    State('state_id', 'value'), 
    State('race_id', 'value')
)
def update_candidate_dropdown(click, name, counties, state_abbr, race_id): 
    # counties += ['']
    # counties = tuple(counties)
    print(counties)
    name += ['']
    name = tuple(name)
    if name == 'TOTAL VOTES': 
        data = mydb.query(f'''
            SELECT distinct MAX(county) as county, max(date) as date, SUM(county_votes) as county_votes, MAX(extracted_at) AS extracted_at
            FROM TFN_DB.primary{race_id}Election2022Histo
            WHERE state_abbr='{state_abbr}' and county='{counties}'
            GROUP BY county, date 
            order by date;
        ''')
    else: 
        data = mydb.query(f'''
            SELECT distinct county, name, county_percent, county_votes, date, extracted_at
            FROM TFN_DB.primary{race_id}Election2022Histo
            WHERE state_abbr='{state_abbr}' and county='{counties}' and name IN {name} order by date;
        ''')
    
    data['date'] = pd.to_datetime(data['date'])
    data = data.drop_duplicates(subset=['county', 'county_votes', 'name'])
    chart = curve.historical_curve(data, 'date', 'county_votes', f'Votes increase on the election period for {", ".join(name)} - {race_id}', 'Vote Increase', 'name', 'bar')
    return chart

