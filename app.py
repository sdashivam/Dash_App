import plotly.graph_objects as go
import plotly.express as px
import dash
import plotly
from dash.dependencies import State, Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.offline as pyo
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


    
dataset = pd.read_csv("D:\MLDL_intrn\practice\Data Set\Data Set\Geo Sales.csv")
dataset.isna().sum().sum()
df = dataset.dropna()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
               meta_tags=[{'name':'viewport',
                          'content':'width=device-width,initial-scale=1.0'}]
               )



app.layout = dbc.Container([


    dbc.Row([

        dbc.Col(

            html.H1(
                "Sales Dashboard",
                className='text-lg-center text-primary mb-4'
            ),
        width=12)
        ],
        align='start' 
    ),

    dbc.Row([

        dbc.Col([

            html.P("Select Country:",
                style={"textDecoration":"underline"}),
            dcc.Checklist(id='checklist1',
                          value=['Australia','United States'],
                         options=[{'label':x, 'value':x}
                                    for x in sorted(df['Country'].unique() )],
                         labelClassName="mr-3"),
            dcc.Graph(id='pie-chart1',figure={}),
        ],#width={'size':5,'offset':1},
          xs=12, sm=12, md=12, lg=6, xl=6
        ),

        dbc.Col([
            html.P("Select Country:",
                style={"textDecoration":"underline"}),
            dcc.Checklist(id='checklist2',
                          value=['Australia','United States'],
                         options=[{'label':x, 'value':x}
                                    for x in sorted(df['Country'].unique() )],
                         labelClassName="mr-3"),
            dcc.Graph(id='hist-graph2', figure={})
        ],#width={'size':5, 'offset':1},
          xs=12, sm=12, md=12, lg=6, xl=6
        )
    ], align="center" ),
    
    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='dpdn1', multi=True, 
                         value=['New South Wales', 'Queensland', 'South Australia'],
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['State'].unique() )],
                        ),
            dcc.Graph(id='ling-fig1', figure={}),
            #html.Button(id='button1', n_clicks=0, children="Graph")
        ],# width={'size':5, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=6, xl=6
        ), 

        dbc.Col([
            dcc.Dropdown(id='dpdn2', multi=True, 
                         value=['Coffs Harbour', 'Darlinghurst', 'Goulburn'],
                         options=[{'label':x, 'value':x}
                         for x in sorted(df['City'].unique() )],
                        ),
            dcc.Graph(id='line-fig2', figure={}),
            #html.Button(id='button2', n_clicks=0, children="Graph")
        ],
           xs=12, sm=12, md=12, lg=6, xl=6
        ),
    ], no_gutters=True, justify='start'),
], fluid=True)


@app.callback(
    Output(component_id='pie-chart1', component_property='figure'),
    [Input(component_id='checklist1', component_property='value')],
    prevent_initial_call = False
     )
    
def pie_graph(selected_country):
    if len(selected_country) > 0:
        print(f"country selected by user:{selected_country}")
        print(type(selected_country))
        dff=df[df['Country'].isin(selected_country)]
        fig = px.pie(dff,names='Country',values='SalesAmount')
        fig.update_traces(textinfo="value+percent").update_layout(title_x=0.5)
        return fig
    elif len(selected_country)==0:
        raise dash.exceptions.PreventUpdate
        


@app.callback(
    Output(component_id='hist-graph2', component_property='figure'),
    [Input(component_id='checklist2', component_property='value')],
    prevent_initial_call = False
     )

def hist_graph(selected_country):
    if len(selected_country) >0:
        print(f"country selected by user:{selected_country}")
        print(type(selected_country))
        dff=df[df['Country'].isin(selected_country)]
        fig = px.histogram(dff,x='Country',y='SalesAmount')
        fig.update_traces(text="value+percent").update_layout(title_x=0.5)
        return fig
    elif len(selected_country)==0:
        raise dash.exceptions.PreventUpdate


        
@app.callback(
    Output(component_id='ling-fig1', component_property='figure'),
    [Input(component_id='dpdn1', component_property='value')],
    prevent_initial_call = False
     )
def line_fig1(selected_state):
    if len(selected_state) >0:
        print(f"state selected by user:{selected_state}")
        print(type(selected_state))
        dff = df[df['State'].isin(selected_state)]
        fig = px.area(dff, x='SalesAmount', y='State',color="Country",orientation="h")
        fig.update_traces(text="value+percent").update_layout(title_x=0.5)
        return fig
    elif len(selected_state)==0:
        raise dash.exceptions.PreventUpdate



@app.callback(
    Output(component_id='line-fig2', component_property='figure'),
    [Input(component_id='dpdn2', component_property='value')],
    prevent_initial_call = False
     )
def line_fig2(selected_city):
    if len(selected_city)>0:
        print(f"city selected by user:{selected_city}")
        print(type(selected_city))
        dff = df[df['City'].isin(selected_city)]
        fig = px.bar(dff,'SalesAmount','City',color='Country')
        return fig
    elif len(selected_city)==0:
         raise dash.exceptions.PreventUpdate
        
        
        
if __name__== '__main__':
    app.run_server()





