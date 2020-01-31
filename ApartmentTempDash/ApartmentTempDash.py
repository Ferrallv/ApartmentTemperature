import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import pandas as pd

df_temps = pd.read_csv('df_temps.csv')
df_temps['Date/Time'] = pd.to_datetime(df_temps['Date/Time'])
df_temps.set_index('Date/Time', inplace=True)


min_date = df_temps.index.min()
max_date = df_temps.index.max()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=dt(min_date.year, min_date.month, min_date.day),
        max_date_allowed=dt(max_date.year, max_date.month, max_date.day),
        initial_visible_month=dt(min_date.year, min_date.month, min_date.day),
        date=dt(min_date.year, min_date.month, min_date.day)
    ),
    
    html.Div(id='output-container-date-picker-single'),
    
    html.Div([
        html.Div([    
            dcc.Graph(id='first_graph')
        ], className="six columns"),
        
        html.Div([
            dcc.Graph(id='second_graph')
        ], className="six columns"),
    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(id='third_graph')
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='fourth_graph')
        ], className="six columns")
    ], className="row")
])

@app.callback(
    [Output('output-container-date-picker-single', 'children'),
     Output('first_graph', 'figure'),
     Output('second_graph', 'figure'),
     Output('third_graph', 'figure'),
     Output('fourth_graph', 'figure')],
    [Input('my-date-picker-single', 'date')])
def update_output(date):
    
    string_prefix = 'Data recorded on: '
    if date is not None:
        date = dt.strptime(date[:10], '%Y-%m-%d')
        date_string = date.strftime('%B %d, %Y')
        
        figure1={
            'data': [{
                'x' : df_temps[(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].index.hour,
                'y' : df_temps['Temp (°C)'][(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].values,
                'mode': 'lines',
                'marker': {'color': 'rgba(178,223,138,1)'},
                'name': 'Outdoor °C'
                    }],
            'layout': dict(
                xaxis={'title': 'Time - 24 Hour'},
                yaxis={'title': 'Outdoor Temperature in °C'},
                title='Outdoor Temperature Over Time',
                height=360
                )
            }
        
        figure2={
            'data': [{
                'x' : df_temps[(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].index.hour,
                'y' : df_temps['Rel Hum (%)'][(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].values,
                'mode': 'lines',
                'marker': {'color': 'rgba(51,160,44,1)'},
                'name': 'Rel Hum (%)'
                    }],
            'layout': dict(
                xaxis={'title': 'Time - 24 Hour'},
                yaxis={'title': 'Relative Humidity (%)'},
                title='Outdoor Relative Humidity Over Time',
                height=360
                )
            }           

        figure3={
            'data': [{
                'x' : df_temps[(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].index.hour,
                'y' : df_temps['kWh'][(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].values,
                'mode': 'lines',
                'marker': {'color': 'rgba(166,206,227,1)'},
                'name': 'kWh'
                    }],
            'layout': dict(
                xaxis={'title': 'Time - 24 Hour'},
                yaxis={'title': 'kWh'},
                title='kWh Usage Over Time',
                height=360
                )
            } 

        figure4={
            'data': [{
                'x' : df_temps[(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].index.hour,
                'y' : df_temps['Apt_Temp'][(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].values,
                'mode': 'lines',
                'marker': {'color': 'rgba(31,120,180,1)'},
                'name' : 'Apartment °C'
                    },
                {
                'x' : df_temps[(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].index.hour,
                'y' : [21 for i in df_temps[(df_temps.index.month == date.month) & (df_temps.index.day == date.day)].index.hour],
                'mode': 'lines',
                'marker': {'color': 'red'},
                'name': 'Legal Minimum °C'
                }],
            'layout': dict(
                xaxis={'title': 'Time - 24 Hour'},
                yaxis={'title': 'Apartment Temperature in °C'},
                title='Apartment Temperature Over Time',
                height=360,
                showlegend=False
                )
            } 
        return string_prefix + date_string, figure1, figure2, figure3, figure4



if __name__ == '__main__':
    app.run_server(debug=True)