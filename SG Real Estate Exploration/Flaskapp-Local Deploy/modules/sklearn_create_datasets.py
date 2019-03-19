def sklearn_create_datasets(regress_df_final):
	data = regress_df_final.copy()
	X = data.drop(['Amenities','Description','Url','RentalRate'], axis=1)
	y = data.RentalRate
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
	ListingTitle_train = X_train.ListingTitle
	ListingTitle_test = X_test.ListingTitle
	X_train.drop('ListingTitle', axis=1, inplace=True)
	X_test.drop('ListingTitle', axis=1, inplace=True)
	return X_train, y_train, X_test, y_test, ListingTitle_train, ListingTitle_test