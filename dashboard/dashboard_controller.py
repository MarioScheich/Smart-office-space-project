import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "knowledge", "knowledge_log.csv")


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Raspberry Pi Sensor Dashboard", style={'textAlign': 'center'}),
    
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Refresh every 5 seconds
        n_intervals=0
    ),

    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='humidity-graph'),
    dcc.Graph(id='co2-graph'),

    html.Div(id='latest-status', style={'marginTop': '20px', 'fontSize': '20px'}),
])

@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('co2-graph', 'figure'),
     Output('latest-status', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    df = pd.read_csv(CSV_FILE)

    # Latest data
    latest = df.iloc[-1]

    # Plot 1: Temperature
    fig_temp = px.line(df, x='timestamp_utc', y=['DHT_temperature', 'temperature'],
                       title='Temperature (DHT vs OpenWeather)',
                       labels={'value': 'Temperature (°C)', 'timestamp_utc': 'Time'})

    # Plot 2: Humidity
    fig_hum = px.line(df, x='timestamp_utc', y=['DHT_Humidity', 'humidity'],
                      title='Humidity (DHT vs OpenWeather)',
                      labels={'value': 'Humidity (%)', 'timestamp_utc': 'Time'})

    # Plot 3: CO2
    fig_co2 = px.line(df, x='timestamp_utc', y='co2_ppm',
                      title='CO2 Levels (ppm)',
                      labels={'co2_ppm': 'CO2 (ppm)', 'timestamp_utc': 'Time'})

    # Latest Status Display
    status = f"""
    Latest Data:
    DHT Temp: {latest['DHT_temperature']}°C | DHT Humidity: {latest['DHT_Humidity']}%
    PIR Motion: {latest['PIR_Motion_state']}
    Weather: {latest['weather_desc']} | Outside Temp: {latest['temperature']}°C
    CO2: {latest['co2_ppm']} ppm | Meeting: {latest['meeting']}
    """

    return fig_temp, fig_hum, fig_co2, status

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
