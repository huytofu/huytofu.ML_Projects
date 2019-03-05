def sklearn_collect_predictions(predictions_train, predictions_test, y_train, y_test, ListingTitle_train, ListingTitle_test):
	columns_train = ListingTitle_train.index
	columns_test = ListingTitle_test.index
	y_train = np.array(y_train)
	y_test = np.array(y_test)
	ListingTitle_train = np.array(ListingTitle_train)
	ListingTitle_test = np.array(ListingTitle_test)
	#print('Predictions for first 5 entries of trainset\n')
	train_df = pd.DataFrame(data=[ListingTitle_train[:5],y_train[:5],predictions_train[:5]], 
							index=['ListingTitle','True RentalRate','RentalRate Prediction in SGD'], columns=columns_train[:5])
	#print('\nPredictions for first 5 entries of testset\n')
	test_df = pd.DataFrame(data=[ListingTitle_test[:5],y_test[:5],predictions_test[:5]], 
						   index=['ListingTitle','True RentalRate','RentalRate Prediction in SGD'], columns=columns_test[:5])
	sample_predictions = dict()
	sample_predictions['train']=train_df.T
	sample_predictions['test']=test_df.T
	return sample_predictions