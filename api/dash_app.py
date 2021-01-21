# import library
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash
import pandas as pd
import numpy as np
from flask import send_file


def createDash(server, pathName):
    # path data
    pathData = './data.csv'
    # load data
    df = pd.read_csv("data.csv", delimiter=",")
    y_predict = pd.read_csv("y_final.csv", delimiter=",")
    y_test = pd.read_csv("y_test.csv", delimiter=",")
    x_test = pd.read_csv("X_test.csv", delimiter=",")

    # preapare data for 3d chart focused on educational-num, age, hours-per-week, income column
    d_normal = x_test
    d_normal['income_>50K'] = y_test['income_>50K']

    d_3d = x_test
    d_3d['income_>50K'] = y_predict['income_>50K']

    # list columns which have only numeric type.
    column_list = list(df.columns)

    # Initialise the app
    app = dash.Dash(__name__, server=server, url_base_pathname=pathName)

    # option list for chart selection
    body_list = ["Explore Each Column", "Explore Relationship Between Columns",
                 "Compare Different Between Original and Predict Data"]

    # callbacks for button-exlore change style main1
    @app.callback(
        Output('main1', 'style'),
        [
            Input('button-explore', 'n_clicks'),
        ]
    )
    def update_main1(n_clicks):
        if not n_clicks or n_clicks == 0:
            raise dash.exceptions.PreventUpdate("cancel the callback")
        else:
            return {'display': 'none'}

    # callbacks for button-exlore change style main2

    @app.callback(
        Output('main2', 'style'),
        [
            Input('button-explore', 'n_clicks'),
        ]
    )
    def update_main2(n_clicks):
        if not n_clicks or n_clicks == 0:
            raise dash.exceptions.PreventUpdate("cancel the callback")
        else:
            return {'display': 'block'}

    # callbacks for download button
    @app.callback(
        Output('button-download', 'style'),
        [
            Input('button-download', 'n_clicks'),
        ]
    )
    def send_file_csv(n_clicks):
        if n_clicks == 0:
            raise dash.exceptions.PreventUpdate("cancel the callback")
        else:
            send_file(pathData,
                      mimetype='text/csv',
                      attachment_filename='downloadFile.csv',
                      as_attachment=True)
            return {}

    # Callback for chart change body
    @app.callback(Output('selector1', 'value'), Output('selector2', 'value'), Output('selector3', 'value'), Output('typeChart', 'style'),
                  Output('originalData', 'style'), Output('predictData', 'style'), Output(
                      'selector1', 'style'), Output('selector2', 'style'), Output('selector3', 'style'),
                  [Input('selector_left', 'value')])
    def update_right_body(selector_left):
        if selector_left == "Explore Each Column":
            return 'age', '', '', {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
        if selector_left == "Explore Relationship Between Columns":
            return 'age', 'educational-num', '', {"display": "block"}, {"display": "block"}, {"display": "none"}, {"display": "block"}, {"display": "block"}, {"display": "none"}
        if selector_left == "Compare Different Between Original and Predict Data":
            return 'age', 'educational-num', 'hours-per-week', {"display": "block"}, {"display": "block"}, {"display": "Block"}, {"display": "block"}, {"display": "block"}, {"display": "block"}
        else:
            return '', '', '', {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

    # Callback for interactive scatterplot
    @app.callback(Output('myChart', 'figure'), Output('myChart2', 'figure'),
                  [Input('selector_left', 'value'), Input('selector1', 'value'), Input('selector2', 'value'), Input('selector3', 'value'), Input('rdbTypeChart', 'value')])
    def update_chart(selector_left, selector1, selector2, selector3, rdbTypeChart):
        # create a backup data
        backup_df = df
        if selector_left == "Explore Relationship Between Columns":
            # return figure for the graph based on column x , y and type of chart.
            if rdbTypeChart == "bar":
                fig = px.bar(backup_df, x=selector1,
                             y=selector2, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                return fig, ''
            if rdbTypeChart == "line":
                fig = px.line(backup_df, x=selector1,
                              y=selector2, color='income_>50K')
                fig.update_layout(transition_duration=500)
                return fig, ''
            if rdbTypeChart == "area":
                fig = px.area(backup_df, x=selector1,
                              y=selector2, color='income_>50K')
                fig.update_layout(transition_duration=500)
                return fig, ''
            if rdbTypeChart == "funnel":
                fig = px.funnel(backup_df, x=selector1,
                                y=selector2, color='income_>50K')
                fig.update_layout(transition_duration=500)
                return fig, ''
            else:
                fig = px.scatter(backup_df, x=selector1,
                                 y=selector2, color='income_>50K')
                fig.update_layout(transition_duration=500)
                return fig, ''
        if selector_left == "Compare Different Between Original and Predict Data":
            # return figure for the graph based on column x , y and type of chart.
            if rdbTypeChart == "bar":
                fig = px.bar(d_normal, x=selector1,
                             y=selector2, color='income_>50K')
                fig2 = px.bar(d_3d, x=selector1,
                              y=selector2, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                fig2.update_layout(transition_duration=500)
                return fig, fig2
            if rdbTypeChart == "line":
                fig = px.line(d_normal, x=selector1,
                              y=selector2, color='income_>50K')
                fig2 = px.line(d_3d, x=selector1,
                               y=selector2, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                fig2.update_layout(transition_duration=500)
                return fig, fig2
            if rdbTypeChart == "area":
                fig = px.area(d_normal, x=selector1,
                              y=selector2, color='income_>50K')
                fig2 = px.area(d_3d, x=selector1,
                               y=selector2, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                fig2.update_layout(transition_duration=500)
                return fig, fig2
            if rdbTypeChart == "funnel":
                fig = px.funnel(d_normal, x=selector1,
                                y=selector2, color='income_>50K')
                fig2 = px.funnel(d_3d, x=selector1,
                                 y=selector2, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                fig2.update_layout(transition_duration=500)
                return fig, fig2
            if rdbTypeChart == "3d":
                fig = px.scatter_3d(d_normal, x=selector1,
                                    y=selector2, z=selector3, color='income_>50K')
                fig2 = px.scatter_3d(d_3d, x=selector1,
                                     y=selector2, z=selector3, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                fig2.update_layout(transition_duration=500)
                return fig, fig2
            else:
                fig = px.scatter(d_normal, x=selector1,
                                 y=selector2, color='income_>50K')
                fig2 = px.scatter(d_3d, x=selector1,
                                  y=selector2, color='income_>50K')
                # set transition when updating the graph to make it display smoothy.
                fig.update_layout(transition_duration=500)
                fig2.update_layout(transition_duration=500)
                return fig, fig2
        else:
            # return figure for the graph based on column y and type of chart.
            fig = px.box(backup_df, y=selector1)
            fig.update_layout(transition_duration=500)
            return fig, ''

    # Define the app
    app.layout = html.Div(
        children=[
            # Main 1: Introduction, main screen
            html.Div(id="main1", className='', style={
                'display': 'block'}, children=[
                html.Div(className="full-screen-body fade-in d-flex align-items-center justify-content-center", children=[
                    html.Div(className="main-intro-body d-flex align-items-center justify-content-center flex-column text-center", children=[
                        html.H1("Dash - Plotly Interactive Visualisation",
                                className="mb-3"),
                        html.H4(
                            "Analyze an income dataset. The dataset provided predictive feature like education , employment status , marital status to predict if the salary is greater than $50K"),
                        html.H4(
                            "With 14 columns (8 categorical, 6 numerical), this dataset will be more than enough for you to get started and explore with Data Science"),
                        html.Div(className="d-flex align-items-center justify-content-center text-center mt-2",
                                 children=[
                                     html.Button("Explore Data",
                                                 id="button-explore", className="mr-2"),
                                     html.Button("Download Dataset",
                                                 id="button-download"),
                                 ])
                    ])
                ])
            ]),
            # Main 2: Chart Screen
            html.Div(id="main2", className='row',  style={
                'display': 'none'},  # Define the row element
                children=[
                # Define the left element
                html.Div(className='three columns div-user-controls',
                         children=[
                             html.H2('Income Dashboard'),
                             html.P(
                                 '''Visualising the bank dataset with Plotly - Dash'''),
                             html.P(
                                 "Choose one option in the dropdown below to exlore the dataset:"),
                             html.Div(className='div-for-dropdown',
                                      children=[
                                          dcc.Dropdown(id='selector_left',
                                                       options=[
                                                           {"label": i,
                                                            "value": i}
                                                           for i in body_list
                                                       ],
                                                       multi=False,
                                                       placeholder="What will you explore?",
                                                       value="",
                                                       ),
                                      ]
                                      ),
                             # create a list of raido buttons for type of chart.
                             html.Div(id='typeChart', className='div-for-dropdown',
                                      children=[
                                          html.P(
                                              '''Please choose a type chart: '''),
                                          dcc.RadioItems(
                                              id='rdbTypeChart',
                                              options=[{'label': i, 'value': i}
                                                       for i in ['scatter', 'line', 'area', 'bar', 'funnel', '3d']],
                                              value='scatter'
                                          )
                                      ]
                                      ),
                             # Adding option to select columns
                             html.Div(className='div-for-dropdown',
                                      children=[
                                          dcc.Dropdown(id='selector1',
                                                       options=[
                                                           {"label": i,
                                                            "value": i}
                                                           for i in column_list
                                                       ],
                                                       multi=False,
                                                       placeholder="Select x column",
                                                       value='age',
                                                       )
                                      ]
                                      ),
                             html.Div(className='div-for-dropdown',
                                      children=[
                                          dcc.Dropdown(id='selector2',
                                                       options=[
                                                           {"label": i,
                                                            "value": i}
                                                           for i in column_list
                                                       ],
                                                       multi=False,
                                                       placeholder="Select y column",
                                                       value='',
                                                       )
                                      ]
                                      ),
                             html.Div(className='div-for-dropdown',
                                      children=[
                                          dcc.Dropdown(id='selector3',
                                                       options=[
                                                           {"label": i,
                                                            "value": i}
                                                           for i in column_list
                                                       ],
                                                       multi=False,
                                                       placeholder="Select y column",
                                                       value='',
                                                       )
                                      ]
                                      ),
                         ]
                         ),
                # Define the right element
                html.Div(className='nine columns', children=[
                    html.Div(id='originalData', className="row", children=[
                        html.H6('Original Data'),
                        dcc.Graph(id='myChart')
                    ]),
                    html.Div(id='predictData', className='row', children=[
                        html.H6('Predict Data'),
                        dcc.Graph(id='myChart2')
                    ])
                ])
            ]
            )
        ]
    )
    return app
