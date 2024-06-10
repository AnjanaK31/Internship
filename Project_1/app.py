import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

file_path = 'Attrition data.csv' 
data = pd.read_csv(file_path)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Employee Attrition Dashboard'), className='mb-2')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='attrition-graph'), className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='department-dropdown', options=[
            {'label': department, 'value': department} for department in data['Department'].unique()
        ], placeholder='Select a Department'), className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='department-attrition-graph'), className='mb-4')
    ])
])

@app.callback(
    Output('attrition-graph', 'figure'),
    Output('department-attrition-graph', 'figure'),
    Input('department-dropdown', 'value')
)
def update_graph(selected_department):
    attrition_fig = px.histogram(data, x='Attrition', title='Attrition Distribution')
    if selected_department:
        dept_data = data[data['Department'] == selected_department]
    else:
        dept_data = data

    department_attrition_fig = px.histogram(dept_data, x='Department', color='Attrition', barmode='group', 
    title=f'Attrition Rate by Department: {selected_department if selected_department else "All"}')

    return attrition_fig, department_attrition_fig

if __name__ == '__main__':
    print("Dash app running at http://127.0.0.1:8050/")