def sklearn_evaluate_results(model, X_train, y_train, X_test, y_test):
	predictions_train = model.predict(X_train)
	predictions_test = model.predict(X_test)
	r2_dict=dict()
	rmse_dict=dict() 
	r2_dict['train']=r2_score(y_train, predictions_train)
	rmse_dict['train']=(mean_squared_error(y_train, predictions_train))**0.5
	r2_dict['test']=r2_score(y_test, predictions_test)
	rmse_dict['test']=(mean_squared_error(y_test, predictions_test))**0.5
	#print('\n****************************************************************************************\n')
	return predictions_train, predictions_test, r2_dict, rmse_dict
