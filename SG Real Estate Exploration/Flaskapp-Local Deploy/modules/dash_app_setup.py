app_dash = dash.Dash(__name__, server=application, url_base_pathname = '/dashboard/')
app_dash.layout = html.Div(dcc.Markdown("# Nothing Here!"))

@application.route('/hahaha', methods=['POST','GET'])
def show_charts():	
	global plot_charts_cue
	global app_dash
	global graph0		
	global graph1		
	global graph2		
	global graph3		
	global graph4		
	if (request.method == 'POST') and plot_charts_cue:
		app_dash.layout = html.Div(style=dict(textAlign="center", display="inline-block"), 
								children=[graph1, graph2, graph3, graph4])
		return flask.redirect('/dashboard/')
	else:
		return render_template('chart_error.html')