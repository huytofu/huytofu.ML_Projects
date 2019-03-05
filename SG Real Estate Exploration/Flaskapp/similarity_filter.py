import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

def run_similarity_filtering(include_amen, amenities_list, regress_df_final, dict2, preference_dict, cat_pref_dict):

	def run_similarity_search(include_amen, amenities_list, regress_df, scaler, dict2, cat_pref_dict, preference_dict):
		df = regress_df.copy()
		df.loc[9999] = [0]*len(df.columns)
		df.ListingTitle.loc[9999] = dict2['ListingTitle']
		df.Area_Sqft.loc[9999] = dict2['Area_Sqft']
		df.Price_psf.loc[9999] = dict2['Price_psf']
		df.RentalRate.loc[9999] = dict2['RentalRate']
		df.NumBeds.loc[9999] = dict2['NumBeds']
		number = dict2['District']
		district = 'District_D' + number
		try: df[district].loc[9999] = 1
		except: pass
		state = dict2['Furnishing']
		furnishing = 'Furnishing_' + state
		try: df[furnishing].loc[9999] = 1
		except: pass
		proptype = dict2['PropertyType']
		property_type = 'PropertyType_' + proptype
		try: df[property_type].loc[9999] = 1
		except: pass
		duration = dict2['Leasedur']
		lease_dur = 'Lease_' + duration
		try: df[lease_dur].loc[9999] = 1
		except: pass
		if include_amen == 'Y':
			df.Amenities.loc[9999] = dict2['Amenities']
			for amenity in amenities_list:
				if amenity in df.Amenities.loc[9999]:
					df[amenity].loc[9999] = 1
		instance = df.loc[9999].copy()
		instance['Summary'] = ','.join([property_type.split('_')[1], district.split('_')[1], furnishing.split('_')[1], lease_dur.split('_')[1]])
		df.drop(['ListingTitle','Url','Description','Amenities'], axis=1, inplace=True)
		scaled = scaler.fit_transform(df)
		df_scaled = pd.DataFrame(data=scaled, columns=df.columns, index=df.index)
		
		scaler_second = MinMaxScaler()
		features = list(preference_dict.keys())
		for feature in features:
			scaler_second.feature_range = (0, preference_dict[feature])
			df_scaled[feature] = scaler_second.fit_transform(np.array(df_scaled[feature]).reshape(-1,1))
		features_cat = list(cat_pref_dict.keys())
		for feature in features_cat:
			scaler_second.feature_range = (0, cat_pref_dict[feature])
			for column in df.columns:
				if feature in column:
					df_scaled[column] = scaler_second.fit_transform(np.array(df_scaled[column]).reshape(-1,1))
				
		knn_filtering = NearestNeighbors(radius=2)
		knn_filtering.fit(df_scaled)
		return knn_filtering, df_scaled, instance, property_type
	
	def return_filter_result(knn, df_scaled, regress_df, instance, property_type, include_amen):
		result_df = regress_df.copy()
		result_df['PropertyType_condo'] = list(map(lambda x,y:1 if (x==0) and (y==0) else 0, 
														result_df['PropertyType_hdb'], result_df['PropertyType_landed']))
		result_df['Lease_24 months'] = 	list(map(lambda x,y,z:1 if (x==0) and (y==0) and (z==0) else 0, 
												result_df['Lease_Flexible'], result_df['Lease_12 months'], result_df['Lease_6 months']))
		filter_result = knn.kneighbors(X=np.array(df_scaled.loc[9999]).reshape(1,-1), return_distance=False)
		output = result_df.iloc[filter_result[0][1:]]
		summary_list=[]
		for j in range(len(output)):
			summary=[]
			for column in output.columns:
				if (output[column].iloc[j] == 1) and ('_' in column): summary.append(column.split('_')[1])
			summary_list.append(','.join(summary))
		output['Summary'] = summary_list
		if include_amen == 'Y':
			output_Url = output['Url'].to_frame()
			output = output[['ListingTitle','Price_psf','RentalRate','NumBeds','Area_Sqft', 'Summary','Amenities']]
			user_input = instance[['ListingTitle','Price_psf','RentalRate','NumBeds','Area_Sqft', 'Summary','Amenities']]
		else:
			output_Url = output['Url'].to_frame()
			output = output[['ListingTitle','Price_psf','RentalRate','NumBeds','Area_Sqft', 'Summary']]
			user_input = instance[['ListingTitle','Price_psf','RentalRate','NumBeds','Area_Sqft', 'Summary']]
		user_input.name = 'Your Proposed Property'
		return user_input, output, output_Url

	regress_df = regress_df_final.copy()
	scaler = MinMaxScaler(feature_range=(0,1))
	knn, df_scaled, instance, property_type = run_similarity_search(include_amen, amenities_list, regress_df, 
																			scaler, dict2, cat_pref_dict, preference_dict)
	user_input, output, output_Url = return_filter_result(knn, df_scaled, regress_df, instance, property_type, include_amen)
	return user_input.to_frame(), output, output_Url