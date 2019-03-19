import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import seaborn as sns
import pandas

def plot_numbeds(new_df,d):
	m=new_df.groupby(by=['PropertyType','NumBeds']).mean().reset_index()
	numbed_list = m['NumBeds'].unique()
	m=m.pivot(index='PropertyType', columns='NumBeds', values=d)
	m.fillna(value=0, inplace=True)

	data2=[]
	prop_type=['condo','hdb','landed']

	for numbed in numbed_list:
		x=[]
		y=[]
		for i in range(3):
			x.append(prop_type[i])
			y.append(m.loc[prop_type[i]][numbed])
		data2.append(go.Bar(x=x, y=y,
					name='{}-Bed'.format(numbed),
					marker=dict(line=dict(color='black', width=1))))
	
	layout2 = go.Layout(title='Interactive Barplot of Avg {} given Num of Bedrooms'.format(d), barmode='group',
					xaxis=dict(title='PropertyType'), yaxis=dict(title=d), height=900, width=1200)
	fig2 = go.Figure(data=data2, layout=layout2)
	graph = html.Div([html.H2('chart2'), dcc.Graph(id='Bar Plot 1', figure=fig2)])
	return graph

def plot_furnishing(new_df,d):
	n=new_df.groupby(by=['PropertyType','Furnishing']).mean().reset_index()
	furnishing_list = n['Furnishing'].unique()
	n=n.pivot(index='PropertyType', columns='Furnishing', values=d)
	n.fillna(value=0, inplace=True)

	data3=[]
	prop_type=['condo','hdb','landed']
	
	for furnishing in furnishing_list:
		x=[]
		y=[]
		for i in range(3):
			x.append(prop_type[i])
			y.append(n.loc[prop_type[i]][furnishing])
		data3.append(go.Bar(x=x, y=y,
					name='{}'.format(furnishing),
					marker=dict(line=dict(color='black', width=1))))
		
	layout3 = go.Layout(title='Interactive Barplot of Avg {} given Furnishing State'.format(d), barmode='group',
					xaxis=dict(title='PropertyType'), yaxis=dict(title=d), height=900, width=1200)
	fig3 = go.Figure(data=data3, layout=layout3)
	graph = html.Div([html.H2('chart3'), dcc.Graph(id='Bar Plot 2', figure=fig3)])
	return graph

def plot_leasedur(new_df,d):
	o=new_df.groupby(by=['PropertyType','Lease']).mean().reset_index()
	lease_list = o['Lease'].unique()
	o=o.pivot(index='PropertyType', columns='Lease', values=d)
	o.fillna(value=0, inplace=True)

	data4=[]
	prop_type=['condo','hdb','landed']
	
	for lease in lease_list:
		x=[]
		y=[]
		for i in range(3):
			x.append(prop_type[i])
			y.append(o.loc[prop_type[i]][lease])
		data4.append(go.Bar(x=x, y=y,
					name='{}'.format(lease),
					marker=dict(line=dict(color='black', width=1))))
		
	layout4 = go.Layout(title='Interactive Barplot of Avg {} given Lease Term'.format(d), barmode='group',
					xaxis=dict(title='PropertyType'), yaxis=dict(title=d), height=900, width=1200)
	fig4 = go.Figure(data=data4, layout=layout4)
	graph = html.Div([html.H2('chart4'), dcc.Graph(id='Bar Plot 3', figure=fig4)])
	return graph