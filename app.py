
# coding: utf-8

# Final project

# The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
# The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' (more here)

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(_name_)
server=app.server

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df=df[~ df['GEO'].str.contains('European' and 'Euro')]

title1 = 'Correlation between indicators (values in current prices, million euros)'
title2 = 'Evolution of indicators (values in current prices, million euros)'

available_indicators = df['NA_ITEM'].unique()
available_countries=df['GEO'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
        ),
# HW2
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown-geo',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Belgium'
            ),
        ],style={'width': '48%', 'display': 'inline-block','margin-bottom' : '35px'}),
        
        html.Div([
            dcc.Dropdown(
                id='dropdown-indi',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block','margin-bottom' : '35px'}),
        
        dcc.Graph(id='country-graphic')
    ])    
    
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    
    dfff = df[df['UNIT']=='Current prices, million euro']
    dff = dfff[dfff['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
    
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            )
            }

@app.callback(
    dash.dependencies.Output('country-graphic','figure'),
    [dash.dependencies.Input('dropdown-geo','value'),
     dash.dependencies.Input('dropdown-indi','value')])

def update_graph2(dropdown_geo_name,dropdown_indi_name):
    dff1 = df[df['UNIT']=='Current prices, million euro']
    dff2 = dff1[dff1['GEO'] == dropdown_geo_name]
    
    return {
        'data': [go.Scatter(
            x=dff2['TIME'].unique(),
            y=dff2[dff2['NA_ITEM'] == dropdown_indi_name]['Value'],
            text=dff2[dff2['NA_ITEM'] == dropdown_indi_name]['TIME'],
            mode='lines',
        )],
        'layout': go.Layout(
            title=title2,
            autosize=True,
            xaxis={
                'title': 'Year'
            },
            yaxis={
                'title': dropdown_indi_name,
            },
            margin={'l': 70, 'b': 50, 't': 50, 'r': 0, 'autoexpand':True},
            hovermode='closest'
        )
        
    }

if __name__ == '__main__':
    app.run_server()

