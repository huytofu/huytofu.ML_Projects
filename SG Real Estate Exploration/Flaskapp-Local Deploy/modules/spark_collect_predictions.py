def spark_collect_predictions(predictions_train, predictions_test):
	sample_predictions = dict()
	#print('Predictions for first 5 entries of trainset\n')
	answer_train = predictions_train.select(['ListingTitle', 'RentalRate', 'RentalRate Prediction in SGD']).take(5)
	sample_predictions['train'] = pd.DataFrame(data=answer_train, columns=['ListingTitle','True RentalRate','RentalRate Prediction in SGD'])
	#print('Prediction for firest 5 entries of testset\n')
	answer_test = predictions_test.select(['ListingTitle', 'RentalRate', 'RentalRate Prediction in SGD']).take(5)
	sample_predictions['test'] = pd.DataFrame(data=answer_test, columns=['ListingTitle','True RentalRate','RentalRate Prediction in SGD'])
	return sample_predictions