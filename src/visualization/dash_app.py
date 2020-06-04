# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from visualisation_functions import filter_dataframe, get_metrics


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

df = pd.read_csv('temp.csv')

state_options = [{'label': state, 'value': state} for state in list(df.state.unique())]

city_options = [{'label': city, 'value': city} for city in list(df.city.unique())]

neighborhood_options = [{'label': nb, 'value': nb} for nb in list(df.neighbor_labels.unique())]


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiZXN0aGVyZ2xvcmlhZGF3ZXMiLCJhIjoiY2pqOW01dGQ4MGI0dDNxbnh3dHVidzM5byJ9.DHl2gDduxDm5OvGi_az5Fg"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Restaurant Performance",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Restaurant Performance",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),

            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [

                        html.P("Filter by state:", className="control_label"),

                        dcc.Dropdown(
                            id="state",
                            options=state_options,
                            multi=True,
                            value='AZ',
                            className="dcc_control",
                        ),

                        html.P("Filter by city:", className="control_label"),

                        dcc.Dropdown(
                            id="city",
                            options=city_options,
                            multi=True,
                            value='Goodyear',
                            className="dcc_control",
                        ),
                        html.P("Filter by neighborhood:", className="control_label"),

                        dcc.Dropdown(
                            id="neighborhood",
                            options=neighborhood_options,
                            multi=True,
                            value='-1',
                            className="dcc_control",
                        ),

                    ],
                    className="pretty_container four column",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="restaurantText"), html.P("No. of Restaurants")],
                                    id="restaurants",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="closureText"), html.P("Closure Rate")],
                                    id="closure",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="starsText"), html.P("Average Stars")],
                                    id="stars",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight column",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

"""
# Helper functions
def human_format(num):
    if num == 0:
        return "0"

    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000 ** magnitude)))
    return mantissa + ["", "K", "M", "G", "T", "P"][magnitude]
"""
# Create callbacks

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)


@app.callback(
    Output("aggregate_data", "data"),
    [
        Input("state", "value"),
        Input("city", "value"),
        Input("neighborhood", "value"),

    ],
)
def update_metric_text(state, city, neighborhood):

    dff = filter_dataframe(df, state, city, int(neighborhood))
    rest, closure, stars, review = get_metrics(dff)
    return [rest, closure, stars, review]


@app.callback(
    [
        Output("restaurantText", "children"),
        Output("closureText", "children"),
        Output("starsText", "children"),
    ],
    [Input("aggregate_data", "data")],
)
def update_text(data):
    return str(data[0]) , str(data[1]), str(data[2])

"""
# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
    [State("lock_selector", "value"), State("main_graph", "relayoutData")],
)
def make_main_figure(
    well_statuses, well_types, year_slider, selector, main_graph_layout
):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    traces = []
    for well_type, dfff in dff.groupby("Well_Type"):
        trace = dict(
            type="scattermapbox",
            lon=dfff["Surface_Longitude"],
            lat=dfff["Surface_latitude"],
            text=dfff["Well_Name"],
            customdata=dfff["API_WellNo"],
            name=WELL_TYPES[well_type],
            marker=dict(size=4, opacity=0.6),
        )
        traces.append(trace)

    # relayoutData is None by default, and {'autosize': True} without relayout action
    if main_graph_layout is not None and selector is not None and "locked" in selector:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            layout["mapbox"]["center"]["lon"] = lon
            layout["mapbox"]["center"]["lat"] = lat
            layout["mapbox"]["zoom"] = zoom

    figure = dict(data=traces, layout=layout)
    return figure


# Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"), [Input("main_graph", "hoverData")])
def make_individual_figure(main_graph_hover):

    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
            ]
        }

    chosen = [point["customdata"] for point in main_graph_hover["points"]]
    index, gas, oil, water = produce_individual(chosen[0])

    if index is None:
        annotation = dict(
            text="No data available",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_individual["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Gas Produced (mcf)",
                x=index,
                y=gas,
                line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Oil Produced (bbl)",
                x=index,
                y=oil,
                line=dict(shape="spline", smoothing=2, width=1, color="#a9bb95"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Water Produced (bbl)",
                x=index,
                y=water,
                line=dict(shape="spline", smoothing=2, width=1, color="#92d8d8"),
                marker=dict(symbol="diamond-open"),
            ),
        ]
        layout_individual["title"] = dataset[chosen[0]]["Well_Name"]

    figure = dict(data=data, layout=layout_individual)
    return figure


# Selectors, main graph -> aggregate graph
@app.callback(
    Output("aggregate_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
        Input("main_graph", "hoverData"),
    ],
)
def make_aggregate_figure(well_statuses, well_types, year_slider, main_graph_hover):

    layout_aggregate = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 31101173130000}
            ]
        }

    chosen = [point["customdata"] for point in main_graph_hover["points"]]
    well_type = dataset[chosen[0]]["Well_Type"]
    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff[dff["Well_Type"] == well_type]["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)

    data = [
        dict(
            type="scatter",
            mode="lines",
            name="Gas Produced (mcf)",
            x=index,
            y=gas,
            line=dict(shape="spline", smoothing="2", color="#F9ADA0"),
        ),
        dict(
            type="scatter",
            mode="lines",
            name="Oil Produced (bbl)",
            x=index,
            y=oil,
            line=dict(shape="spline", smoothing="2", color="#849E68"),
        ),
        dict(
            type="scatter",
            mode="lines",
            name="Water Produced (bbl)",
            x=index,
            y=water,
            line=dict(shape="spline", smoothing="2", color="#59C3C3"),
        ),
    ]
    layout_aggregate["title"] = "Aggregate: " + WELL_TYPES[well_type]

    figure = dict(data=data, layout=layout_aggregate)
    return figure


# Selectors, main graph -> pie graph
@app.callback(
    Output("pie_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
def make_pie_figure(well_statuses, well_types, year_slider):

    layout_pie = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    selected = dff["API_WellNo"].values
    index, gas, oil, water = produce_aggregate(selected, year_slider)

    aggregate = dff.groupby(["Well_Type"]).count()

    data = [
        dict(
            type="pie",
            labels=["Gas", "Oil", "Water"],
            values=[sum(gas), sum(oil), sum(water)],
            name="Production Breakdown",
            text=[
                "Total Gas Produced (mcf)",
                "Total Oil Produced (bbl)",
                "Total Water Produced (bbl)",
            ],
            hoverinfo="text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(colors=["#fac1b7", "#a9bb95", "#92d8d8"]),
            domain={"x": [0, 0.45], "y": [0.2, 0.8]},
        ),
        dict(
            type="pie",
            labels=[WELL_TYPES[i] for i in aggregate.index],
            values=aggregate["API_WellNo"],
            name="Well Type Breakdown",
            hoverinfo="label+text+value+percent",
            textinfo="label+percent+name",
            hole=0.5,
            marker=dict(colors=[WELL_COLORS[i] for i in aggregate.index]),
            domain={"x": [0.55, 1], "y": [0.2, 0.8]},
        ),
    ]
    layout_pie["title"] = "Production Summary: {} to {}".format(
        year_slider[0], year_slider[1]
    )
    layout_pie["font"] = dict(color="#777777")
    layout_pie["legend"] = dict(
        font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"
    )

    figure = dict(data=data, layout=layout_pie)
    return figure


# Selectors -> count graph
@app.callback(
    Output("count_graph", "figure"),
    [
        Input("well_statuses", "value"),
        Input("well_types", "value"),
        Input("year_slider", "value"),
    ],
)
def make_count_figure(well_statuses, well_types, year_slider):

    layout_count = copy.deepcopy(layout)

    dff = filter_dataframe(df, well_statuses, well_types, [1960, 2017])
    g = dff[["API_WellNo", "Date_Well_Completed"]]
    g.index = g["Date_Well_Completed"]
    g = g.resample("A").count()

    colors = []
    for i in range(1960, 2018):
        if i >= int(year_slider[0]) and i < int(year_slider[1]):
            colors.append("rgb(123, 199, 255)")
        else:
            colors.append("rgba(123, 199, 255, 0.2)")

    data = [
        dict(
            type="scatter",
            mode="markers",
            x=g.index,
            y=g["API_WellNo"] / 2,
            name="All Wells",
            opacity=0,
            hoverinfo="skip",
        ),
        dict(
            type="bar",
            x=g.index,
            y=g["API_WellNo"],
            name="All Wells",
            marker=dict(color=colors),
        ),
    ]

    layout_count["title"] = "Completed Wells/Year"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = False
    layout_count["autosize"] = True

    figure = dict(data=data, layout=layout_count)
    return figure
"""

# Main
if __name__ == "__main__":
    app.run_server(debug=True)