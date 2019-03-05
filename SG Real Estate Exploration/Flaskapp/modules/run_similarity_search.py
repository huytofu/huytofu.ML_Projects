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