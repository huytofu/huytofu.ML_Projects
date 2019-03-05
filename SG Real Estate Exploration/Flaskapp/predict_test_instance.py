import numpy as np
import pandas as pd

def predict_test_instance(choose_session, include_amen, amenities_list, model, 
						need_transformer, transformer, assembler, sc, dict1, regress_df_final):
	
	def predict_new_instance_spark(include_amen, amenities_list, model, assembler, sc, dict1, regress_df_final):
		df = regress_df_final.iloc[[0,1]]
		df.loc[9999]=[0]*len(df.columns)
		if include_amen == 'Y':
			df.Amenities.loc[9999] = dict1['Amenities']
			for amenity in amenities_list:
				if amenity in df.Amenities.loc[9999]:
					df[amenity].loc[9999] = 1
		else:
			df.Amenities.loc[9999] = ''
		df.Description = ''
		df.Url = ''
		df.ListingTitle.loc[9999] = dict1['ListingTitle']
		df.Area_Sqft.loc[9999] = dict1['Area_Sqft']
		df.Price_psf.loc[9999] = dict1['Price_psf']
		df.NumBeds.loc[9999] = dict1['NumBeds']
		number = dict1['District']
		district = 'District_D' + number
		try: df[district].loc[9999] = 1
		except: pass
		state = dict1['Furnishing']
		furnishing = 'Furnishing_' + state
		try: df[furnishing].loc[9999] = 1
		except: pass
		proptype = dict1['PropertyType']
		property_type = 'PropertyType_' + proptype
		try: df[property_type].loc[9999] = 1
		except: pass
		duration = dict1['Leasedur']
		lease_dur = 'Lease_' + duration
		try: df[lease_dur].loc[9999] = 1
		except: pass
		instance = sc.createDataFrame(df.iloc[[2,1]])
		assembled = assembler.transform(instance)
		assembled_prediction = model.transform(assembled)
		answer = assembled_prediction.select(['ListingTitle', 'RentalRate Prediction in SGD']).take(1)
		test_df = pd.DataFrame(data=answer, index=['Test Instance'],
								columns=['ListingTitle','RentalRate Prediction in SGD'])
		sc.stop()
		return test_df

	def predict_new_instance_sklearn(include_amen, amenities_list, model, need_transformer, transformer, dict1, regress_df_final):
		df = regress_df_final.iloc[[0,1]]
		df.loc[9999]=[0]*len(df.columns)
		if include_amen == 'Y':
			df.Amenities.loc[9999] = dict1['Amenities']
			for amenity in amenities_list:
				if amenity in df.Amenities.loc[9999]:
					df[amenity].loc[9999] = 1 
		else: pass
		df.Area_Sqft.loc[9999] = dict1['Area_Sqft']
		df.Price_psf.loc[9999] = dict1['Price_psf']
		df.NumBeds.loc[9999] = dict1['NumBeds']
		number = dict1['District']
		district = 'District_D' + number
		try: df[district].loc[9999] = 1
		except: pass
		state = dict1['Furnishing']
		furnishing = 'Furnishing_' + state
		try: df[furnishing].loc[9999] = 1
		except: pass
		proptype = dict1['PropertyType']
		property_type = 'PropertyType_' + proptype
		try: df[property_type].loc[9999] = 1
		except: pass
		duration = dict1['Leasedur']
		lease_dur = 'Lease_' + duration
		try: df[lease_dur].loc[9999] = 1
		except: pass
		instance_Title = dict1['ListingTitle']
		instance_X = df.drop(['Amenities','Description','Url','ListingTitle','RentalRate'], axis=1).loc[9999]
		if need_transformer:
			instance_X = transformer(instance_X)
		prediction = model.predict(np.array(instance_X).reshape(1,-1))[0]
		test_df = pd.DataFrame(data=[instance_Title,prediction], columns=['Test Instance'],
							   index=['ListingTitle','RentalRate Prediction in SGD'])
		return test_df

	if choose_session == 'Sklearn':
		return predict_new_instance_sklearn(include_amen, amenities_list, model, need_transformer, transformer, dict1, regress_df_final)
	else:
		return predict_new_instance_spark(include_amen, amenities_list, model, assembler, sc, dict1, regress_df_final)

	