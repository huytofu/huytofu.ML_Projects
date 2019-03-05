import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor as SklearnForest
from sklearn.ensemble import GradientBoostingRegressor as SklearnGBT
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.feature_selection import f_regression

def run_sklearn_session(regress_df_final, model_choice, model_dict):
	
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

	def sklearn_create_model(X_train, y_train, X_test, y_test, model_choice, model_dict):
		need_transformer = False
		transformer = None
		if model_choice == 'KNN':
			need_transformer = True
			scaler = MinMaxScaler()
			X_train = scaler.fit_transform(X_train)
			X_test = scaler.transform(X_test)
			n_neighbors = model_dict['NumNeighbors']
			knn = KNeighborsRegressor(n_neighbors=n_neighbors)
			transformer = (lambda x: scaler.transform(np.array(x).reshape(1,-1)))
			fitted_model = knn.fit(X_train, y_train)
		elif model_choice == 'Linear':
			sig_level = model_dict['SigLevel']
			regress_type = model_dict['Regularizor']
			regParam = model_dict['RegParam']
			if regress_type == 'Ridge':
				need_transformer = True
				_, pvalues = f_regression(X_train, y_train)
				to_remove=[]
				featureCols = X_train.columns
				for i in range(len(pvalues)):
					if pvalues[i] > sig_level:
						to_remove.append(featureCols[i])
				#		print('---Insignificant feature! p = {:0.4f} - {}---'.format(pvalues[i], featureCols[i]))		
				#print('Features with p_value > {} are discarded'.format(sig_level))
				#print('\n****************************************************************************************\n')
				X_train.drop(to_remove, axis=1, inplace=True)
				X_test.drop(to_remove, axis=1, inplace=True)
				transformer = (lambda x:x.to_frame().T.drop(to_remove, axis=1))
				linearmodel = Ridge(alpha=regParam)
			else:
				#print('Lasso model automatically selects relevant features')
				#print('\n****************************************************************************************\n')
				linearmodel = Lasso(alpha=regParam)
			fitted_model = linearmodel.fit(X_train, y_train)
		elif model_choice == 'Quadratic':
			#print('''Each feature x will be transformed into 2 features = x & x^2. 
			#		Number of features is therefore doubled. Interaction terms are not included''')
			#print('\n****************************************************************************************\n')
			need_transformer = True
			polyconverter = PolynomialFeatures(degree=2, include_bias=False)
			intermed_train = polyconverter.fit_transform(np.array(X_train).reshape(-1,1))
			intermed_test = polyconverter.fit_transform(np.array(X_test).reshape(-1,1))
			X_train = intermed_train.reshape(X_train.shape[0], X_train.shape[1]*2)
			X_test = intermed_test.reshape(X_test.shape[0], X_test.shape[1]*2)
			sig_level = model_dict['SigLevel']
			regress_type = model_dict['Regularizor']
			regParam = model_dict['RegParam']
			if regress_type == 'Ridge':
				_, pvalues = f_regression(X_train, y_train)
				to_include=[]
				for i in range(len(pvalues)):
					if pvalues[i] <= sig_level:
						to_include.append(i)
				#print('Features with p_value > {} are discarded'.format(sig_level))
				#print('\n****************************************************************************************\n')
				X_train = X_train[:,to_include]
				X_test = X_test[:,to_include]
				step1 = (lambda x: polyconverter.fit_transform(np.array(x).reshape(-1,1)))
				transformer = (lambda x: step1(x).reshape(1,-1)[:,to_include])
				linearmodel = Ridge(alpha=regParam)
			else:
				#print('Lasso model automatically selects relevant features')
				#print('\n****************************************************************************************\n')
				step1 = (lambda x: polyconverter.fit_transform(np.array(x).reshape(-1,1)))
				transformer = (lambda x: step1(x).reshape(1,-1))
				linearmodel = Lasso(alpha=regParam)
			fitted_model = linearmodel.fit(X_train, y_train)
		elif model_choice == 'RandomForest':
			numTrees = model_dict['NumTrees']
			maxDepth = model_dict['MaxDepth']
			feature_strat = model_dict['FeatureStrat']
			forest = SklearnForest(n_estimators=numTrees, max_depth=maxDepth, 
										   max_features=feature_strat, n_jobs=4)
			fitted_model = forest.fit(X_train, y_train)
		elif model_choice == 'GBT':
			numTrees = model_dict['NumTrees']
			maxDepth = model_dict['MaxDepth']
			gbt = SklearnGBT(n_estimators=numTrees, max_depth=maxDepth)
			fitted_model = gbt.fit(X_train, y_train)
		#print('Model is done being fitted!')
		#print('\n****************************************************************************************\n')
		return fitted_model, X_train, y_train, X_test, y_test, need_transformer, transformer
	
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


	X_train, y_train, X_test, y_test, ListingTitle_train, ListingTitle_test = sklearn_create_datasets(regress_df_final)
	model, X_train, y_train, X_test, y_test, need_transformer, transformer = sklearn_create_model(X_train, y_train, X_test, y_test, model_choice, model_dict)
	predictions_train, predictions_test, r2_dict, rmse_dict = sklearn_evaluate_results(model, X_train, y_train, X_test, y_test)
	sample_predictions = sklearn_collect_predictions(predictions_train, predictions_test, y_train, y_test, ListingTitle_train, ListingTitle_test)
	return model, need_transformer, transformer, sample_predictions, r2_dict, rmse_dict