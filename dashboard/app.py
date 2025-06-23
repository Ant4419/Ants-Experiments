import os
from dash import Dash, html

DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 8050))

app = Dash(__name__)
app.layout = html.Div([html.H1("Dashboard Service Running!")])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=DASHBOARD_PORT)
