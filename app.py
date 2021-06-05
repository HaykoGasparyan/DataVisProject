import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

data_2016=pd.read_csv('Happiness/2016.csv')
data_2017=pd.read_csv('Happiness/2017.csv')
data_2015=pd.read_csv('Happiness/2015.csv')
data_2018=pd.read_csv('Happiness/2018.csv')
data_2019=pd.read_csv('Happiness/2019.csv')

# Some data preprocessing 
data_2015 = data_2015.drop(['Standard Error', 'Region', 'Dystopia Residual'],axis=1)
data_2015.columns = ['Country', 'Happiness Rank', 'Happiness Score',
                   'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)',
                   'Freedom', 'Generosity','Trust (Government Corruption)']
data_2015['Year'] = 2015

data_2016 = data_2016.drop(['Lower Confidence Interval', 'Upper Confidence Interval', 'Region', 'Dystopia Residual'],axis=1)
data_2016.columns = ['Country', 'Happiness Rank', 'Happiness Score',
                   'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)',
                   'Freedom', 'Generosity','Trust (Government Corruption)']
data_2016['Year'] = 2016

data_2017 = data_2017.drop(['Whisker.low', 'Whisker.high', 'Dystopia.Residual'],axis=1)
data_2017.columns = ['Country', 'Happiness Rank', 'Happiness Score',
                   'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)',
                   'Freedom', 'Generosity','Trust (Government Corruption)']
data_2017['Year'] = 2017

data_2018 = data_2018[['Country or region', 'Overall rank', 'Score', 'GDP per capita',
                                      'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
                                      'Generosity', 'Perceptions of corruption']]
data_2018.columns = ['Country', 'Happiness Rank', 'Happiness Score',
                     'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)',
                     'Freedom', 'Generosity', 'Trust (Government Corruption)']
data_2018['Year'] = 2018

data_2019 = data_2019[['Country or region', 'Overall rank', 'Score', 'GDP per capita',
                                      'Social support', 'Healthy life expectancy', 'Freedom to make life choices',
                                      'Generosity', 'Perceptions of corruption']]
data_2019.columns = ['Country', 'Happiness Rank', 'Happiness Score',
                     'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)',
                     'Freedom', 'Generosity', 'Trust (Government Corruption)']
data_2019['Year'] = 2019

overall_data = pd.concat([data_2015, data_2016, data_2017, data_2018, data_2019])



# Creating options lists

num_cols = ['Happiness Score', 'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 'Freedom',
             'Generosity', 'Trust (Government Corruption)']
year_cols = ['2015', '2016', '2017', '2018', '2019', 'All']
year_cols_2 = ['2015', '2016', '2017', '2018', '2019']


features = [{'label': i, 'value': i} for i in overall_data.columns]
years = [{'label': i, 'value': i} for i in year_cols]
num_options = [{'label': i, 'value': i} for i in num_cols]

years_2 = [{'label': i, 'value': i} for i in year_cols_2]

# One fixed figure

corr_matrix = overall_data[num_cols].corr()
figure_2 = px.imshow(np.abs(corr_matrix), title='Correlation Heatmap')

app = dash.Dash(external_stylesheets = external_stylesheets)

app.layout = html.Div([
            html.Div([html.H1('Happiness Data Analysis')], className = 'row'),
            html.Div([dcc.Dropdown(
                                id = 'features_input',
                                options = features, value = features[2]['value'], className='six columns'),
                     dcc.Dropdown(
                                id = 'years_input',
                                options = years, value = years[0]['value'], className='six columns')],
                 
                 className = 'twelve columns'),
                
            html.Div([
                   html.Div([dcc.Graph(id='Fig1')], className = 'twelve columns'),
            ], className = 'row'),
            html.Div([
                   html.Div([dcc.Graph(figure=figure_2)], className = 'twelve columns'),
            ], className = 'row'),
            html.Div([dcc.Dropdown(
                                id = 'var1',
                                options = num_options, value = num_options[0]['value'], className='six columns'),
                     dcc.Dropdown(
                                id = 'var2',
                                options = num_options, value = num_options[1]['value'], className='six columns')],
                 
                 className = 'twelve columns'),
            html.Div([
                   html.Div([dcc.Graph(id='Fig3')], className = 'twelve columns'),
            ], className = 'row'),
    
            html.Div([dcc.Dropdown(
                                id = 'var3',
                                options = num_options, value = num_options[0]['value'], className='six columns'),
                     dcc.Dropdown(
                                id = 'var4',
                                options = years_2, value = years_2[0]['value'], className='six columns')],
                 
                 className = 'twelve columns'),
            html.Div([
                   html.Div([dcc.Graph(id='Fig4')], className = 'twelve columns'),
            ], className = 'row'),
            html.Div([dcc.Dropdown(
                                id = 'var5',
                                options = years_2, value = years_2[0]['value'], className='six columns'),
                     dcc.Dropdown(
                                id = 'var6',
                                options = num_options, value = num_options[0]['value'], className='six columns')],
                 
                 className = 'twelve columns'),
            html.Div([
                   html.Div([dcc.Graph(id='Fig5')], className = 'twelve columns'),
            ], className = 'row')], className = 'container')


@app.callback(
       Output(component_id = 'Fig1', component_property = 'figure'),
       
        [Input(component_id = 'features_input', component_property = 'value'),
         Input(component_id = 'years_input', component_property = 'value')]         
)

def update_hist(input_1, input_2):
    if(input_2 != 'All'):
        data = overall_data[overall_data['Year'] == int(input_2)]
    else:
        data = overall_data
        
    figure_1 = px.histogram(data, x=input_1, title='Distribution of {}'.format(input_1), nbins=20)
    return figure_1

@app.callback(
       Output(component_id = 'Fig3', component_property = 'figure'),
         [Input(component_id = 'var1', component_property = 'value'),
         Input(component_id = 'var2', component_property = 'value')]
         
)

def update_scatter(input_3, input_4):
    figure_2 = px.scatter(overall_data, x=input_3, y=input_4, title='Scatter plot of {} and {} variables'.format(input_3, input_4))
    
    return figure_2


@app.callback(
       Output(component_id = 'Fig4', component_property = 'figure'),

       [Input(component_id = 'var3', component_property = 'value'),
        Input(component_id = 'var4', component_property = 'value')]
)

def update_bar(input_1, input_2):
    if(input_2 != 'All'):
        data = overall_data[overall_data['Year'] == int(input_2)]
    else:
        data = overall_data
       
    data = data[['Country', input_1]]
    data = data.sort_values(by=input_1)[-30:]
   
    figure = px.bar(data, x='Country', y=input_1, title='Barplot of {} in {}'.format(input_1, input_2))
    return figure


@app.callback(
        Output(component_id = 'Fig5', component_property = 'figure'),

       [Input(component_id = 'var5', component_property = 'value'),
        Input(component_id = 'var6', component_property = 'value')] 
)
    
def update_map(input_1, input_2):
    year_data = overall_data[overall_data['Year']==int(input_1)]
                             
    data = go.Choropleth(
    locations = year_data['Country'],
    locationmode = 'country names',
    z = year_data[input_2],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255, 255, 255)',
            width = 1.5,
        )
    ),
    colorbar = go.choropleth.ColorBar(
        title = 'Score'
        )
    )

    layout = go.Layout(
        geo = go.layout.Geo(
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'

        )
    )


    fig = go.Figure(data = data, layout = layout)
    return fig
                             
                            

if __name__ == '__main__':
    app.run_server(debug = True)