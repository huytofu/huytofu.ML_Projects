def spark_evaluate_results(fitted_model, trainset, testset):
	evaluator2 = RegressionEvaluator(labelCol="RentalRate", predictionCol="RentalRate Prediction in SGD", metricName="rmse")
	evaluator1 = RegressionEvaluator(labelCol="RentalRate", predictionCol="RentalRate Prediction in SGD", metricName="r2")
	predictions_train = fitted_model.transform(trainset)
	predictions_test = fitted_model.transform(testset)
	r2_dict=dict()
	rmse_dict=dict() 
	r2_dict['train'] = evaluator1.evaluate(predictions_train)
	rmse_dict['train'] = evaluator2.evaluate(predictions_train)
	r2_dict['test'] = evaluator1.evaluate(predictions_test)
	rmse_dict['test'] = evaluator2.evaluate(predictions_test)
	#print('\n****************************************************************************************\n')
	return predictions_train, predictions_test, r2_dict, rmse_dict
