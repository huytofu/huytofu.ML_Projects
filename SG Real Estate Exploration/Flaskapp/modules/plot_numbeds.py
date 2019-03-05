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