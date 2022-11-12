from app import app
from components import Home
from dash import html
from dash import dcc


server = app.server


app.layout = html.Div([
        dcc.Store(id='house_data'),
        # dcc.Store(id='nextPageToken', data=None),
        Home.layout
    ], className='w3-container w3-section'
)

if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
