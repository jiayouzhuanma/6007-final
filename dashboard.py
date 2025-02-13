import dash
from dash import dcc, html, Input, Output
import requests
import pandas as pd
import plotly.express as px

# Flask API URL
API_URL = "http://127.0.0.1:5000"

# Initialize Dash app
app = dash.Dash(__name__)

# Dash Layout
app.layout = html.Div([
    html.H1("Smart Meter Dashboard", style={'textAlign': 'center'}),

    # Query Meter Readings
    html.Div([
        html.H3("Query Meter Readings"),
        html.Label("Enter Meter ID:"),
        dcc.Input(id="query_meter_id", type="text", placeholder="e.g. 123-456-789"),
        html.Button("Fetch Data", id="query_button", n_clicks=0),
        dcc.Graph(id="meter_reading_graph")
    ], style={'border': '1px solid #ddd', 'padding': '10px', 'margin': '10px'})
])

# Callback to update the graph
@app.callback(
    Output("meter_reading_graph", "figure"),
    Input("query_button", "n_clicks"),
    Input("query_meter_id", "value")
)
def query_meter_readings(n_clicks, meter_id):
    if n_clicks > 0 and meter_id:
        response = requests.get(f"{API_URL}/meter-reading/{meter_id}")
        if response.status_code == 200:
            data = response.json()["readings"]
            if data:
                df = pd.DataFrame(data)
                fig = px.line(df, x="timestamp", y="kwh", title=f"Meter Readings for {meter_id}")
                return fig
    return px.line(title="No Data Available")

# Run Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
