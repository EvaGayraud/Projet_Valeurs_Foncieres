import plotly.express as px
from data_sources import source_choice
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

PICKLE_DATASET_PATH = "_tmp_dataset.pkl"

try:
    df = pd.read_pickle(PICKLE_DATASET_PATH)
except FileNotFoundError:
    df = source_choice()
    df.to_pickle(PICKLE_DATASET_PATH)

app.layout = html.Div(
    [
        html.H1("DVF Paris", style={"text-align": "center"}),
        dcc.Dropdown(
            id="year",
            options=[
                {"label": "2016", "value": 2016},
                {"label": "2017", "value": 2017},
                {"label": "2018", "value": 2018},
                {"label": "2019", "value": 2019},
                {"label": "2020", "value": 2020},
            ],
            multi=False,
            value="2020",
            style={"width": "40%"},
        ),
        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(id="dispersion", figure={}),
    ]
)


@app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="dispersion", component_property="figure"),
    ],
    [Input(component_id="year", component_property="value")],
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["year"] == option_slctd]

    fig = px.box(dff, x="Commune", y="Valeur fonciere", hover_name="Surface reelle bati")

    return container, fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
