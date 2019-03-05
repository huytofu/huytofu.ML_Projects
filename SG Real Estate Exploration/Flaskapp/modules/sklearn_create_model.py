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