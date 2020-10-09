import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import bystate
from apps import multiselect

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/multiselect':
        return multiselect.layout
    elif pathname == '/bystate':
        return bystate.layout
    else:
        return bystate.layout

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',threaded=False)
