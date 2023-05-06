from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from weather import get_df_euro_AQI, clean_df_euro_AQI, air_quality_table

# read csv file which we before get them by weather.py and save in src
df = pd.read_csv('src/air_quality.csv')
# create a figure of bar 
fig = px.bar(df,
             x='city name',
             y=['good', 'fair', 'moderate', 'poor', 'very poor'],
             color_discrete_sequence=[
                 'green', '#0caf15', 'yellow', 'red', '#9d0d12'],
             text='value')
# create a Dash App
app = Dash(__name__)
# defined the late of the dash app
app.layout = html.Div([
    # set the namae of the Dashboard
    html.H1(children='Air-Quality-Dashboard', style={'textAlign': 'center'}),
    # get the info about first Graph
    html.H3(
        " # Compare cities' air Quality from '22-08-05' to '23-01-05' at one Graph:"),
    # defined a bargraph with the fig we defined before
    dcc.Graph(figure=fig),
    # get the info aboout second Graph
    html.H3(' # Select your desired city for look insight:'),
    # defined a Dropdown input to get the desired city from user
    dcc.Dropdown(df['city name'], 'Dubai', id='dropdown-selection'),
    # using the callback to defined piechart for second graph
    dcc.Graph(id='graph-content'),
    # get info to user for thired graph
    html.Div([
        html.H3(' # Search your desired city for look insight:'),
        html.H4('Enter City Name:'),
        # defind a text input for get name city from user
        dcc.Input(
            id="search-city", type="text",
            placeholder="Isfahan", debounce=True),
        # get info to user for geting date range
        html.H4('Select Date Range:'),
        html.H6('limited from "2022-08-05" to Today!'),
        # defined a date picker range for get date range from user
        dcc.DatePickerRange(
            id="date-picker",
            start_date="2023-04-01",
            end_date="2023-05-01",
            min_date_allowed="2022-08-05",
            max_date_allowed="2023-12-31",
        )
    ]),
    # call the graph
    dcc.Graph(id='graph-searched-city')
])

# callback for second graph barchart
# input: from dropdown-selection id
# output: call graph by graph-content id
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):

    # get a copy of dataframe and clear it for showing in graph
    dff = df[df['city name'] == value]
    i = dff.index
    dff = dff.T[3:]
    dff = dff.rename_axis('Air Quality')
    dff['Days'] = dff[i]
    # return pie chart to second graph
    return px.pie(dff, names=dff.index, values=dff['Days'], title="The European Air Quality Index (AQI)",
                  color=dff.index,
                  color_discrete_sequence=['green', '#0caf15', 'yellow', 'red', '#9d0d12'])

#  callback for third graph
# input from text input for name of city
# input get date range with data-picker 
@callback(
    Output('graph-searched-city', 'figure'),
    Input('search-city', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_search_graph(value, start_date, end_date):
    # get the dataframe info by call get_df_euro_AQI function, it calls API
    df_search = get_df_euro_AQI(value, start_date, end_date)
    # clean a dataframe for show in graph
    df_search = clean_df_euro_AQI(df_search)
    dff = pd.DataFrame(air_quality_table(df_search, value), index=[0])
    dff = dff.T[2:]
    dff = dff.rename_axis('Air Quality')
    dff['Days'] = dff[0]
    # return a barchart for third graph
    return px.bar(dff, x=dff.index, y=dff['Days'], title="The European Air Quality Index (AQI)",
                  color=dff.index,
                  color_discrete_sequence=['green', '#0caf15', 'yellow', 'red', '#9d0d12'])


if __name__ == '__main__':
    app.run_server(debug=True)
