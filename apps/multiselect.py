import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import json
import surveil
#d=open('static_cases.json','r')
#j=json.loads(d.read())
#d.close()
states=['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','YC','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','US','UT','VT','VA','WA','WV','WI','WY']
#select_causes=['Coronavirus Disease 2019','Influenza and pneumonia','Chronic lower respiratory diseases','Adult respiratory distress syndrome','Respiratory failure','Respiratory arrest','Other diseases of the respiratory system','Hypertensive diseases','Ischemic heart disease','Cardiac arrest','Cardiac arrhythmia','Heart failure','Cerebrovascular diseases','Other diseases of the circulatory system','Sepsis','Malignant neoplasms','Diabetes','Obesity','Alzheimer disease','Vascular and unspecified dementia','Renal failure','Intentional and unintentional injury, poisoning and other adverse events','All other conditions and causes (residual)']
select_causes=['Alzheimer disease and dementia','Cerebrovascular diseases','Heart failure','Hypertensive dieases','Ischemic heart disease','Other diseases of the circulatory system','Malignant neoplasms','Diabetes','Renal failure','Sepsis','Chronic lower respiratory disease','Influenza and pneumonia','Other diseases of the respiratory system','Residual (all other natural causes)']
##jurisdiction is a state abbreviation string, e.g., 'YC' or 'NY' or 'DC' or 'TX'
#global placeholder var
p_df=pd.DataFrame({})

from app import app

def get_figure(jurisdictions,causes):
	global p_df
	p_df=pd.DataFrame(surveil.multi(jurisdictions,causes))
	fig = px.bar(p_df, x="week_ending", y="observed", text="alarm")
	fig.update_traces(textposition="outside")
	fig.add_scatter(x=p_df.week_ending,y=p_df.upperbound,name="95% CI upper bound")
	fig.add_scatter(x=p_df.week_ending,y=p_df.lowerbound,name="95% CI lower bound")
	return fig
layout = html.Div([
    html.H2('Covid-related Dash'),
    html.Div(
	[
		dcc.Checklist(
			id="States",
			options=[{'label':i,'value':i} for i in states],
			value=['TX','CA']),
		dcc.Checklist(
			id="causes",
			options=[{'label':i,'value':i} for i in select_causes],
			value=['Alzheimer disease and dementia'])
	],
	style={'width':'90%','display':'inline-block'}),
    html.Div([html.A(
	html.Button(
	'submit',
	id='submit_button',
	n_clicks=0
	)
    )
    ]),
    html.H3('App Description'),
    html.Div(
	[
	html.P('This application allows you to explore CDC mortality data from July 2020, by arbitrarily summing deaths attributed to multiple causes in multiple states.'),
		html.Ul([
			html.Li(['The blue bars sum the reported deaths counts attributed to the causes you select in the states that you select. ',html.A('View CDC Data',href='https://data.cdc.gov/NCHS/Weekly-counts-of-death-by-jurisdiction-and-cause-o/u6jv-9ijr/', target='blank')]),
			html.Li(['The lines give you the upper and lower bounds of the 95% confidence interval on predicted deaths, which is calculated using a Farrington algorithm on the previous 3 years of CDC data.',
				html.Ul([
					html.Li(html.A('Official R Surveillance Package',href='https://cran.r-project.org/web/packages/surveillance/',target='blank')),
					html.Li(html.A('R Surveillance package that this site runs on,modified to show lower bound of confidence interval.',href='https://github.com/JohnMulligan/surveillance-1')),
				]),
			html.Li(['You can explore the same data on a state-by-state basis on ',html.A('this alternative dashboard',href='/bystate')])
		]),
	],
	style={'width':'50%','display':'inline-block'}
    )
    ]),
    dcc.Graph(id='covid-graph-multi'),
])
@app.callback(dash.dependencies.Output('covid-graph-multi','figure'),[dash.dependencies.Input('submit_button','n_clicks')],[dash.dependencies.State('States','value'),dash.dependencies.State('causes','value')]
)

def update_graph(submit_button,States,causes):
	
	ctx=dash.callback_context
	figure = get_figure(States,causes)
	return figure
	
