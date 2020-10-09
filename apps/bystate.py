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
#select_causes=['Alzheimer disease and dementia','Cerebrovascular diseases','Heart failure','Hypertensive dieases','Ischemic heart disease','Other diseases of the circulatory system','Malignant neoplasms','Diabetes','Renal failure','Sepsis','Chronic lower respiratory disease','Influenza and pneumonia','Other diseases of the respiratory system','Residual (all other natural causes)']
##causes have been updated yet again
select_causes=['Alzheimer disease and dementia','Cerebrovascular diseases','Heart failure','Hypertensive diseases','Ischemic heart disease','Other diseases of the circulatory system','Malignant neoplasms','Diabetes','Renal failure','Sepsis','Chronic lower respiratory disease','Influenza and pneumonia','Other diseases of the respiratory system']
##jurisdiction is a state abbreviation string, e.g., 'YC' or 'NY' or 'DC' or 'TX'
#global placeholder var
p_df=pd.DataFrame({})

from app import app

def get_figure(jurisdiction,cause):
	print(jurisdiction)
	global p_df
	p_df=pd.DataFrame(surveil.bystate(jurisdiction))
	f_df=p_df[p_df['cause_group']==cause]
	title = "Deaths attributed to %s in %s" %(cause,jurisdiction)
	fig = px.bar(f_df, x="week_ending", y="observed", text="alarm",
		labels = {"observed":"Deaths","week_ending":"Week Ending Date"},
		title = title)
	fig.update_traces(textposition="outside")
	fig.add_scatter(x=f_df.week_ending,y=f_df.upperbound,name="95% CI upper bound")
	fig.add_scatter(x=f_df.week_ending,y=f_df.lowerbound,name="95% CI lower bound")
	return fig
def filter_figure(State,cause):
	print(cause)
	global p_df
	f_df=p_df[p_df['cause_group']==cause]
	title = "Deaths attributed to %s in %s" %(cause,State)
	fig = px.bar(f_df, x="week_ending", y="observed", text="alarm",
		labels = {"observed":"Deaths","week_ending":"Week Ending Date"},
		title = title)
	fig.update_traces(textposition="outside")
	fig.add_scatter(x=f_df.week_ending,y=f_df.upperbound,name="95% CI upper bound")
	fig.add_scatter(x=f_df.week_ending,y=f_df.lowerbound,name="95% CI lower bound")
	return fig
#borrowing from https://pbpython.com/plotly-dash-intro.html

layout = html.Div([
    html.H2('Covid-related Dash: Select Recorded and Predicted Deaths by State & Imputed Cause'),
    html.Div(
	[
		dcc.Dropdown(
			id="State",
			options=[{'label':i,'value':i} for i in states],
			value='TX'),
		dcc.Dropdown(
			id="cause",
			options=[{'label':i,'value':i} for i in select_causes],
			value='Alzheimer disease and dementia')
	],
	style={'width':'90%','display':'inline-block'}),
	html.H3('App Description'),
	html.Div(
	[
	html.P('This application allows you to explore CDC mortality data from October 7 2020. Selecting a state and then an imputed cause of death will return the number of deaths attributed to that cause in that state, with historical trendlines. Outliers in the positive direction are flagged.'),
		html.Ul([
                        html.Li('State selection is slow. It calculates the trends for every attributed cause of death in the state going back 3 years.'),
			html.Li('Cause selection is fast. It filters the mortality stats for that state, which have already been calculated.'),
			html.Li(['The blue bars show the reported deaths counts attributed to the cause you select in the state you select. ',html.A('View CDC Data',href='https://data.cdc.gov/NCHS/Weekly-counts-of-death-by-jurisdiction-and-cause-o/u6jv-9ijr/', target='blank')]),
			html.Li(['The lines give you the upper and lower bounds of the 95% confidence interval on predicted deaths, which is calculated using a Farrington algorithm on the previous 3 years of CDC data.',
				html.Ul([
					html.Li(html.A('Official R Surveillance Package',href='https://cran.r-project.org/web/packages/surveillance/',target='blank')),
					html.Li(html.A('R Surveillance package that this site runs on,modified to show lower bound of confidence interval.',href='https://github.com/JohnMulligan/surveillance-1',target='blank')),
				]),
			html.Li(['Bars are flagged with an X when they exceed the confidence interval on the predicted trend. In a normal year, for instance, there is a 2.5% chance that any given week will be above a 95% CI\'s upper bound when the full tally is made (which can take up to a year in normal circumstances according to the NCHS).']),
			html.Li(['You can explore the same data by arbitrarily combining states and caues on ',html.A('this alternative dashboard',href='/multiselect')])
		]),
	],
	style={'width':'80%','display':'inline-block'}
    )]),


    dcc.Graph(id='covid-graph-bystate'),
])
@app.callback(dash.dependencies.Output('covid-graph-bystate','figure'),[dash.dependencies.Input('State','value'),dash.dependencies.Input('cause','value')])
def update_graph(State,cause):
	ctx=dash.callback_context
	if ctx.triggered[0]['prop_id'].split('.')[0]=='cause':
		#cheap
		figure = filter_figure(State,cause)
	else:
		#costly
		figure = get_figure(State,cause)
	
	return figure
	
if __name__ == '__main__':
	app.run_server(debug=True,host='0.0.0.0',threaded=False)

