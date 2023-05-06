from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from weather import get_df_euro_AQI, clean_df_euro_AQI, air_quality_table

df = pd.read_csv('src/air_quality.csv')

fig = px.bar(df,
             x='city name',
             y=['good', 'fair', 'moderate', 'poor', 'very poor'],
             color_discrete_sequence=[
                 'green', '#0caf15', 'yellow', 'red', '#9d0d12'],
             text='value')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Air-Quality-Dashboard', style={'textAlign': 'center'}),
    html.H3(
        " # Compare cities' air Quality from '22-08-05' to '23-01-05' at one Graph:"),
    # dash_table.DataTable(
    #     df.to_dict('records'),
    #     [{"name": i, "id": i} for i in df.columns if i != 'Unnamed: 0' and  i!= 'total day']),
    dcc.Graph(figure=fig),
    html.H3(' # Select your desired city for look insight:'),
    dcc.Dropdown(df['city name'], 'Dubai', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    # html.Div(children='Search your desired city for look insight:'),
    # dcc.Input(id="search-city", type="text", placeholder="Isfahan", debounce=True),
    html.Div([
        html.H3(' # Search your desired city for look insight:'),
        html.H4('Enter City Name:'),
        dcc.Input(
            id="search-city", type="text",
            placeholder="Isfahan", debounce=True),
        html.H4('Select Date Range:'),
        html.H6('limited from "2022-08-05" to Today!'),
        dcc.DatePickerRange(
            id="date-picker",
            start_date="2023-04-01",
            end_date="2023-05-01",
            min_date_allowed="2022-08-05",
            max_date_allowed="2023-12-31",
        )
    ]),
    # dcc.Input(id='search-city', 'Isfahan'),
    dcc.Graph(id='graph-searched-city')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):

    dff = df[df['city name'] == value]
    i = dff.index
    print(dff.head())
    dff = dff.T[3:]
    dff = dff.rename_axis('Air Quality')
    dff['Days'] = dff[i]
    print(dff.columns)

    return px.pie(dff, names=dff.index, values=dff['Days'], title="The European Air Quality Index (AQI)",
                  color=dff.index,
                  color_discrete_sequence=['green', '#0caf15', 'yellow', 'red', '#9d0d12'])

    # return px.bar(dff, x=dff.index, y=dff['Days'], title="The European Air Quality Index (AQI)",
    #               color=dff.index,
    #               color_discrete_sequence=['green', '#0caf15', 'yellow', 'red', '#9d0d12'])


@callback(
    Output('graph-searched-city', 'figure'),
    Input('search-city', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_search_graph(value, start_date, end_date):
    # df_search = get_df_euro_AQI(value, start_date='2022-08-05', end_date='2023-01-05')
    df_search = get_df_euro_AQI(value, start_date, end_date)
    # transfer dataframe
    df_search = clean_df_euro_AQI(df_search)
    # get the result and transfer to dataframe- it dictionary={'good': 0, 'fair': 0, 'moderate': 0, 'poor': 0, 'very poor': 0, 'total day': 0}
    dff = pd.DataFrame(air_quality_table(df_search, value), index=[0])
    print(dff.head())
    dff = dff.T[2:]
    print(dff.head())
    dff = dff.rename_axis('Air Quality')
    dff['Days'] = dff[0]
    print(dff.columns)
    return px.bar(dff, x=dff.index, y=dff['Days'], title="The European Air Quality Index (AQI)",
                  color=dff.index,
                  color_discrete_sequence=['green', '#0caf15', 'yellow', 'red', '#9d0d12'])


if __name__ == '__main__':
    app.run_server(debug=True)
