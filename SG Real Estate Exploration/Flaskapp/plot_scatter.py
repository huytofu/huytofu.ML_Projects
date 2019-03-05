import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import seaborn as sns
import pandas

def plot_static_scatter(new_df):
	graph = sns.pairplot(data=new_df, x_vars=['Area_Sqft','Price_psf','RentalRate'], y_vars=['Area_Sqft','Price_psf','RentalRate'],
				hue = 'PropertyType', hue_order=['condo','landed','hdb'], height=4)
	return graph

def plot_interactive_scatter(new_df,a,b,c):
	data1=[]
	plot_data=new_df[new_df.PropertyType==a]
	for i in range(len(plot_data)):
		data1.append(go.Scatter(x=[plot_data[b].iloc[i]],
							y=[plot_data[c].iloc[i]],
							mode='markers',
							showlegend=False, 
							hoverinfo=['x+y+text'],
							marker=dict(size=6, color='blue', line=dict(color='black', width=1)),
							text='Name={}, Location={}\n, Index={}'.format(plot_data.ListingTitle.iloc[i], 
																			plot_data.District.iloc[i],
																			plot_data.iloc[i].name)))
		
		
	layout1 = go.Layout(title='Interactive Scatter Plot of {} vs {} - of {} Property Type'.format(b,c,a.upper()),
					  xaxis=dict(title=b), yaxis=dict(title=c), hovermode='closest', height=1000, width=1000)
	fig1 = go.Figure(data=data1, layout=layout1)
	graph = html.Div([html.H2('chart1'), dcc.Graph(id='Scatter Plot', figure=fig1)])
	return graph