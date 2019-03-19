import dash
import flask
import pandas as pd
import numpy as np
import plot_scatter as scatter
import plot_barchart as barchart
import predict_rent as pr
import similarity_filter as sf
import dash_html_components as html
import dash_core_components as dcc
from flask import Flask, request, render_template
from wtforms import Form, validators
from wtforms.fields import FloatField, IntegerField, TextField, SubmitField
from utils import create_final_df, modify_df

class ReusableForm(Form):
	Condo_Rent_Min = FloatField("Enter Condo's Min Rental Rate in SGD:",validators=[validators.InputRequired()])
	Condo_Rent_Max = FloatField("Enter Condo's Max Rental Rate in SGD:",validators=[validators.InputRequired()])
	Landed_Rent_Min = FloatField("Enter Landed Prop's Min Rental Rate in SGD:",validators=[validators.InputRequired()])
	Landed_Rent_Max = FloatField("Enter Landed Prop's Max Rental Rate in SGD:",validators=[validators.InputRequired()])
	HDB_Rent_Min = FloatField("Enter The HDB's Min Rental Rate in SGD:",validators=[validators.InputRequired()])
	HDB_Rent_Max = FloatField("Enter The HDB's Max Rental Rate in SGD:",validators=[validators.InputRequired()])
	submit = SubmitField("Submit")

class ChartForm(Form):
	submit_chart = SubmitField("Here")

class AmenForm(Form):
	submit_choice = SubmitField("Here")

class ReusableForm_Predict_Rent(Form):
	ListingTitle_A = TextField("Please Enter Listing Title",validators=[validators.InputRequired()])
	Area_Sqft_A = FloatField("Enter The Unit's Area In Square Feet:",validators=[validators.InputRequired()])
	Price_psf_A = FloatField("Enter The Unit's Price Per Squared Feet In SGD:",validators=[validators.InputRequired()])
	NumTrees_A = IntegerField('Enter Number of Trees in Random Forest Model',
					validators=[validators.NumberRange(min=1, max=200, message='Please choose between 1 and 200 for Forest NumTrees!'),
								validators.Optional(strip_whitespace=True)])
	NumTrees_B = IntegerField('Enter Number of Trees in GBT Model',
					validators=[validators.NumberRange(min=1, max=200, message='Please choose between 1 and 200 for GBT NumTrees!'),
								validators.Optional(strip_whitespace=True)])
	MaxDepth_A = IntegerField('Enter MaxDepth of Tree in Random Forest Model (<=30 for Sklearn session)',
					validators=[validators.NumberRange(min=1, max=100, message='Please choose between 1 and 100 for Forest MaxDepth!'),
								validators.Optional(strip_whitespace=True)])
	MaxDepth_B = IntegerField('Enter MaxDepth of Tree in GBT Model',
					validators=[validators.NumberRange(min=1, max=10, message='Please choose between 1 and 10 for GBT MaxDepth! GBT consists of slow learners only'),
								validators.Optional(strip_whitespace=True)])
	NumNeighbors = IntegerField('Enter Number of Neighbors for KNN Model',
					validators=[validators.NumberRange(min=1, max=200, message='Please choose between 1 and 200 NearestNeighbors! More neighbors = very slow program'),
								validators.Optional(strip_whitespace=True)])
	SigLevel = FloatField("Enter The SigLevel for Pvalues of Features in Linear/Quadratic Model:",
					validators=[validators.NumberRange(min=0, max=1, message='Please choose between 0 and 1 for SigLevel!'),
								validators.Optional(strip_whitespace=True)])
	RegParam = FloatField("Enter The Regularization Parameter in Linear/Quadratic Model (recommended = 1):",
					validators=[validators.NumberRange(min=0, max=10, message='Please choose Regularization Param between 0 and 10!'),
								validators.Optional(strip_whitespace=True)])
	Amenities_A = TextField("Enter Amenities In This Unit (Skip If Choosing To Not Include)")
	submit_A = SubmitField("Submit")

class ReusableForm_SimFilter(Form):
	
	ListingTitle_B = TextField("Please Enter Listing Title",validators=[validators.InputRequired()])
	Area_Sqft_B = FloatField("Enter The Unit's Area In Square Feet:",validators=[validators.InputRequired()])
	Price_psf_B = FloatField("Enter The Unit's Price Per Squared Feet In SGD:",validators=[validators.InputRequired()])
	RentalRate = FloatField("Enter The Unit's Rental Rate in SGD:",
					validators=[validators.NumberRange(min=100, max=60000, message='Please choose between 100 and 60000 for RentalRate!'),
								validators.InputRequired()])
	Amenities_B = TextField("Enter Amenities In This Unit (Skip If Choosing To Not Include)")
	submit_B = SubmitField("Submit")

full_df = pd.read_csv('Cleaned_combined_Listings.csv')
pd.set_option('display.max_colwidth',200)
graph1=None
graph2=None
graph3=None
graph4=None
plot_charts_cue = False
display_text=''
display_thankyou=''
new_df=''
include_amen=''
img_src='static/nothing_here.png'

application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app_dash = dash.Dash(__name__, server=application, url_base_pathname = '/dashboard/')
app_dash.layout = html.Div(dcc.Markdown("# Nothing Here!"))

@application.route('/', methods=['POST','GET'])
def home():
	global full_df
	global new_df
	global include_amen
	global plot_charts_cue
	global display_text
	global display_thankyou
	global graph1		
	global graph2		
	global graph3		
	global graph4		

	form1 = ReusableForm(request.form)
	form2 = ReusableForm_Predict_Rent(request.form)
	form3 = ReusableForm_SimFilter(request.form)
	form4 = ChartForm(request.form)
	form_amen = AmenForm(request.form)

	if (request.method == 'POST'):
		if request.form['form_name'] == 'form1':
			if form1.submit.data and form1.validate():
				property_type = request.form['property_type']
				feature_1 = request.form['feature_1']
				feature_2 = request.form['feature_2']
				feature_3 = request.form['feature_3']
				dict0=dict()
				dict0['Condo_Rent_Min'] = float(request.form['Condo_Rent_Min'])
				dict0['Condo_Rent_Max'] = float(request.form['Condo_Rent_Max'])
				dict0['Landed_Rent_Min'] = float(request.form['Landed_Rent_Min'])
				dict0['Landed_Rent_Max'] = float(request.form['Landed_Rent_Max'])
				dict0['HDB_Rent_Min'] = float(request.form['HDB_Rent_Min'])
				dict0['HDB_Rent_Max'] = float(request.form['HDB_Rent_Max'])
				
				new_df = modify_df(full_df, dict0)
				graph1 = scatter.plot_interactive_scatter(new_df, a=property_type, b=feature_1, c=feature_2)
				graph2 = barchart.plot_numbeds(new_df,d=feature_3)
				graph3 = barchart.plot_furnishing(new_df, d=feature_3)
				graph4 = barchart.plot_leasedur(new_df, d=feature_3)
				plot_charts_cue = True
				display_text = "Dataset done modified. Charts' parameters done established!"
				return render_template('index.html', form1=form1,  form2=form2, form3=form3, form4=form4, form_amen=form_amen,
													Condo_Rent_Min=dict0['Condo_Rent_Min'],
													Condo_Rent_Max=dict0['Condo_Rent_Max'],
													Landed_Rent_Min=dict0['Landed_Rent_Min'],
													Landed_Rent_Max=dict0['Landed_Rent_Max'],
													HDB_Rent_Min=dict0['HDB_Rent_Min'],
													HDB_Rent_Max=dict0['HDB_Rent_Max'],
													plot_charts_cue=plot_charts_cue,
													display_text=display_text,
													display_thankyou=display_thankyou) 

		elif request.form['form_name'] == 'form_amen':
			include_amen = request.form['include_amen']
			if include_amen not in ('Y','N'):
				display_thankyou = 'Please Choose Y or N only! Again!'
			else: display_thankyou = 'Choice {} Submitted! Thank You!'.format(include_amen)

		elif request.form['form_name'] == 'form2':
			if form2.submit_A.data and (type(new_df)==str):
				return render_template ('error.html')
			elif form2.submit_A.data and (include_amen==''):
				return render_template ('error_amen.html')
			elif form2.submit_A.data and form2.validate(): 	
				choose_session = request.form['choose_session']
				if choose_session == 'Sklearn':
					model_choice = request.form['model_choice_sklearn']
				else:
					model_choice = request.form['model_choice_pyspark']
				model_dict=dict()
				if model_choice == 'KNN':
					model_dict['NumNeighbors'] = int(request.form['NumNeighbors'])
				elif model_choice == 'Linear' or model_choice == 'Quadratic':
					model_dict['SigLevel'] = float(request.form['SigLevel'])
					model_dict['Regularizor'] = request.form['Regularizor']
					model_dict['RegParam'] = float(request.form['RegParam'])
				elif model_choice == 'RandomForest':
					model_dict['NumTrees'] = int(request.form['NumTrees_A'])
					model_dict['MaxDepth'] = int(request.form['MaxDepth_A'])
					model_dict['FeatureStrat'] = request.form['FeatureStrat']
				elif model_choice == 'GBT':
					model_dict['NumTrees'] = int(request.form['NumTrees_B'])
					model_dict['MaxDepth'] = int(request.form['MaxDepth_B'])
				
				dict1 = dict()
				dict1['ListingTitle'] = request.form['ListingTitle_A']
				dict1['Area_Sqft'] = float(request.form['Area_Sqft_A'])
				dict1['Price_psf'] = float(request.form['Price_psf_A'])
				dict1['Amenities'] = request.form['Amenities_A']
				dict1['District'] = request.form['District_A']
				dict1['NumBeds'] = int(request.form['NumBeds_A'])
				dict1['Furnishing'] = request.form['Furnishing_A']
				dict1['Leasedur'] = request.form['Leasedur_A']
				dict1['PropertyType'] = request.form['PropertyType_A']
				
				amenities_list, regress_df_final = create_final_df(new_df, include_amen)
				prediction, sample_predictions, r2_dict, rmse_dict = pr.run_rental_rate_prediction(choose_session, include_amen, 
																								amenities_list, regress_df_final, 
																								dict1, model_choice, model_dict)
				return render_template('prediction_result.html', prediction=prediction.to_html(),
																choose_session=choose_session,
																model_choice=model_choice,
																train_rmse=rmse_dict['train'],
																test_rmse=rmse_dict['test'],
																train_r2=r2_dict['train'],
																test_r2=r2_dict['test'],
																sample_predictions_train=sample_predictions['train'].to_html(),
																sample_predictions_test=sample_predictions['test'].to_html(),
																include_amen=include_amen,
																title=dict1['ListingTitle'],
																area=dict1['Area_Sqft'],
																price_psf=dict1['Price_psf'],
																amenities=dict1['Amenities'],
																district=dict1['District'],
																numbeds=dict1['NumBeds'],
																furnishing=dict1['Furnishing'],
																proptype=dict1['PropertyType'],
																lease=dict1['Leasedur'])

		elif request.form['form_name'] == 'form3':
			if form3.submit_B.data and (type(new_df)==str):
				return render_template('error.html')
			elif form3.submit_B.data and (include_amen==''):
				return render_template ('error_amen.html')
			elif form3.submit_B.data and form3.validate():
				dict2 = dict()
				preference_dict=dict()
				cat_pref_dict=dict()
				preference_dict['Area_Sqft'] = float(request.form['Area_Sqft_Importance'])
				preference_dict['Price_psf'] = float(request.form['Price_psf_Importance'])
				preference_dict['RentalRate'] = float(request.form['RentalRate_Importance'])
				preference_dict['NumBeds'] = float(request.form['NumBeds_Importance'])
				cat_pref_dict['PropertyType'] = float(request.form['PropertyType_Importance'])
				cat_pref_dict['District'] = float(request.form['District_Importance'])
				cat_pref_dict['Furnishing'] = float(request.form['Furnishing_Importance'])
				cat_pref_dict['Lease'] = float(request.form['Lease_Importance'])
				cat_pref_dict['Amenities'] = float(request.form['Amenities_Importance'])
				translate={1:'Normal',0.005:"NotRelevant",0.25:'VeryLow',0.5:'Low',2:'High',4:'VeryHigh',
							200:'AsCloseAsPossible',10000:'MustBeSimilar'}

				dict2['ListingTitle'] = request.form['ListingTitle_B']
				dict2['Area_Sqft'] = float(request.form['Area_Sqft_B'])
				dict2['Price_psf'] = float(request.form['Price_psf_B'])
				dict2['RentalRate'] = float(request.form['RentalRate'])
				dict2['Amenities'] = request.form['Amenities_B']
				dict2['District'] = request.form['District_B']
				dict2['NumBeds'] = int(request.form['NumBeds_B'])
				dict2['Furnishing'] = request.form['Furnishing_B']
				dict2['Leasedur'] = request.form['Leasedur_B']
				dict2['PropertyType'] = request.form['PropertyType_B']
				
				amenities_list, regress_df_final = create_final_df(new_df, include_amen)
				user_input, output, output_Url = sf.run_similarity_filtering(include_amen, amenities_list, regress_df_final, 
																dict2, preference_dict, cat_pref_dict)
				return render_template('filtering_result.html', input=user_input.to_html(), 
																output=output.to_html(),
																output_Url=output_Url.to_html(),
																include_amen=include_amen,
																Area_Sqft_pref=translate[preference_dict['Area_Sqft']],
																Price_psf_pref=translate[preference_dict['Price_psf']],
																RentalRate_pref=translate[preference_dict['RentalRate']],
																NumBeds_pref=translate[preference_dict['NumBeds']],
																PropertyType_pref=translate[cat_pref_dict['PropertyType']],
																District_pref=translate[cat_pref_dict['District']],
																Furnishing_pref=translate[cat_pref_dict['Furnishing']],
																Lease_pref=translate[cat_pref_dict['Lease']],
																Amenities_pref=translate[cat_pref_dict['Amenities']]) 

	return render_template('index.html', form1=form1, form2=form2, form3=form3, form4=form4, form_amen=form_amen,
										plot_charts_cue=plot_charts_cue,
										display_text=display_text,
										display_thankyou=display_thankyou)

@application.route('/hahaha', methods=['POST','GET'])
def show_charts():	
	global plot_charts_cue
	global app_dash
	global graph1		
	global graph2		
	global graph3		
	global graph4		
	if (request.method == 'POST') and plot_charts_cue:
		app_dash.layout = html.Div(style=dict(textAlign="center", display="inline-block"), 
								children=[graph1, graph2, graph3, graph4])
		return flask.redirect('/dashboard/')
	else: return render_template('chart_error.html')

@application.route('/seaborn', methods=['POST','GET'])
def seaborn():
	global img_src
	global new_df
	global plot_charts_cue
	if (request.method == 'POST') and plot_charts_cue:
		graph0 = scatter.plot_static_scatter(new_df)
		graph0.savefig('static/scatter.png')
		img_src = 'static/scatter.png'
		return render_template('seaborn_chart.html', img_src=img_src)
	else: return render_template('chart_error.html')

'''
@application.after_request
def no_cache(response):
    """
    Not cache the rendered page for any minute.
    """
    #response = make_response(*args, **kwargs)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
'''   
if __name__ == '__main__':
	application.run(port=8080, debug=True)	
		