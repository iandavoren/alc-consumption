import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.colors

data = pd.read_csv("data/Alcohol_Consumption_US.csv")


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("US Alcohol Consumption by State"),
    
    #dropdown beer/wine/spirit/all
    dcc.Dropdown(
        id='alcohol-type',
        options=[
            {'label': 'Beer', 'value': 'Beer (Per capita consumption)'},
            {'label': 'Wine', 'value': 'Wine (Per capita consumption)'},
            {'label': 'Spirits', 'value': 'Spirits (Per capita consumption)'},
            {'label': 'All beverages', 'value': 'All beverages (Per capita consumption)'}
        ],
        value='All beverages (Per capita consumption)',
        clearable=False,
        style={'width': '50%'}
    ),
    
    #yearslider
    dcc.Slider(
        id='year-slider',
        min=1977,
        max=2016,
        value=1977,
        marks={str(year): str(year) for year in range(1977, 2017, 5)},
        step=1
    ),
    
    #graph
    dcc.Graph(id='consumption-bar-chart')
])

#update chart
@app.callback(
    Output('consumption-bar-chart', 'figure'),
    Input('alcohol-type', 'value'),
    Input('year-slider', 'value')
)
def update_bar_chart(selected_type, selected_year):
    filtered_data = data[data['Year'] == selected_year]
    
    #color_sequence = plotly.colors.sample_colorscale("Viridis", [n/50 for n in range(50)])

    fig = px.bar(
        filtered_data,
        x=selected_type,
        y='State_abbrev',
        #color='State_abbrev', 
        orientation='h',
        title=f'{selected_type} by State in {selected_year}',
        labels={selected_type: 'Per Capita Consumption', 'State_abbrev': 'State'},
        #color_discrete_sequence=color_sequence  

    )
    
    if selected_type == "Beer (Per capita consumption)":
        x_axis_range = [0, 2.5]
    elif selected_type == "Wine (Per capita consumption)":
        x_axis_range = [0, 1.5]
    elif selected_type == "Spirits (Per capita consumption)":
        x_axis_range = [0, 4]
    else:
        x_axis_range = [0, 6.5]

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis=dict(title="Per Capita Consumption", range=x_axis_range),
        #xaxis_title="Per Capita Consumption",
        yaxis_title="State",
        height=1200,
        margin=dict(l=50, r=50, t=50, b=50)   
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
