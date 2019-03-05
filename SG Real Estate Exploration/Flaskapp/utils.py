import pandas as pd

def modify_df(full_df, dict0):
	a=dict0['Condo_Rent_Min']
	b=dict0['Condo_Rent_Max']
	c=dict0['Landed_Rent_Min']
	d=dict0['Landed_Rent_Max'] 
	e=dict0['HDB_Rent_Min']
	f=dict0['HDB_Rent_Max']
	new_df = full_df[((full_df.PropertyType=='condo')&(full_df.RentalRate>=a)&(full_df.RentalRate<=b))|
				((full_df.PropertyType=='landed')&(full_df.RentalRate>=c)&(full_df.RentalRate<=d))|
				((full_df.PropertyType=='hdb')&(full_df.RentalRate>=e)&(full_df.RentalRate<=f))]
	return new_df

def create_final_df(new_df, include_amen):
	
	def transform_categorical_features(new_df):
		regress_df_final = new_df.drop(labels=['NumBaths'], axis=1)
		print('Carrying out transforming categorical features...')
		print('\n********************************************************\n')
		regress_df_final = pd.get_dummies(data=regress_df_final, columns=['District','Furnishing','Lease','PropertyType'])
		matrix=regress_df_final.corr()
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				if abs(matrix.iloc[i][j]) >= 0.7 and i<j:
					print('{} highly correlated with {}. Corr value = _____{}'.format(matrix.index[i], matrix.index[j], matrix.iloc[i,j]))
		print('To remove one category from each highly correlated category pair\nAs well as at least 1 category from each categorical feature')
		print('Features dropped = {} & {} & {} & {}'.format('Furnishing_Partially Furnished', 'Lease_24 months',
															'District_D01', 'PropertyType_condo'))
		regress_df_final.drop(labels=['Furnishing_Partially Furnished', 'Lease_24 months'], axis=1, inplace=True)
		regress_df_final.drop(labels=['District_D01', 'PropertyType_condo'], axis=1, inplace=True)
		return regress_df_final
	
	def treating_amenities(include_amen, amenities_list, regress_df_final):
		if include_amen == 'Y':
			amenities_list_minus = amenities_list.copy()
			amenities_list_minus.remove('No Mention')
			regress_df_final_with_amen = regress_df_final.copy()
			for amenity in amenities_list_minus:
				regress_df_final_with_amen[amenity] = regress_df_final.Amenities.apply(lambda x:1 if amenity in x else 0)
			return regress_df_final_with_amen
		else:
			return regress_df_final

	new_df.Amenities = new_df.Amenities.apply(str)
	amenities_list = []
	if include_amen == 'Y':
		for i in range(len(new_df)):
			amenities_list += new_df.Amenities.iloc[i].split(',')
		amenities_list=list(set(amenities_list))
		amenities_list.sort()
	else: pass
	df_temp = transform_categorical_features(new_df)
	final_df = treating_amenities(include_amen, amenities_list, df_temp)
	return amenities_list, final_df