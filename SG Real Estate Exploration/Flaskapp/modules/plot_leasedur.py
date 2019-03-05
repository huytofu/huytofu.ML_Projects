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