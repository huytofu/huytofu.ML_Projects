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