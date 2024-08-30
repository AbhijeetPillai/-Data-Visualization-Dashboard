import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import io
import base64

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Sales Dashboard'),

    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV'),
        multiple=False
    ),
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[],
        placeholder='Select X-axis'
    ),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[],
        placeholder='Select Y-axis'
    ),
    dcc.Dropdown(
        id='color-dropdown',
        options=[],
        placeholder='Select Color'
    ),
    dcc.Graph(
        id='example-graph'
    )
])

@app.callback(
    [Output('x-axis-dropdown', 'options'),
     Output('y-axis-dropdown', 'options'),
     Output('color-dropdown', 'options'),
     Output('x-axis-dropdown', 'value'),
     Output('y-axis-dropdown', 'value'),
     Output('color-dropdown', 'value'),
     Output('example-graph', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graph(contents, filename):
    if contents is None:
        return [], [], [], None, None, None, {}

    # Decode the uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Update dropdown options based on the CSV file
    columns = [{'label': col, 'value': col} for col in df.columns]
    x_options = columns
    y_options = columns
    color_options = columns

    # Default values for dropdowns
    x_value = df.columns[0] if len(df.columns) > 0 else None
    y_value = df.columns[1] if len(df.columns) > 1 else None
    color_value = df.columns[2] if len(df.columns) > 2 else None

    # Create the bar chart
    if x_value and y_value:
        fig = px.bar(df, x=x_value, y=y_value, color=color_value, barmode='group')
    else:
        fig = {}

    return x_options, y_options, color_options, x_value, y_value, color_value, fig

if __name__ == '__main__':
    app.run_server(debug=True)

