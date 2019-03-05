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