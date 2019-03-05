def spark_create_model(trainset, testset, featureCols, assembler, model_choice, model_dict):
	try:
		trainset = trainset.drop('features2')
		testset = testset.drop('features2')
	except: pass
	if model_choice == 'Linear':
		sig_level = model_dict['SigLevel']
		regress_type = model_dict['Regularizor']
		regParam = model_dict['RegParam']
		if regress_type == 'Ridge':
			elasticNetParam = 0
		else:
			elasticNetParam = 1
		linear = SparkLinear(regParam=regParam, elasticNetParam=elasticNetParam, featuresCol='features', 
							labelCol='RentalRate', predictionCol = 'RentalRate Prediction in SGD')
		fitted_model = linear.fit(trainset)
		if regress_type == 'Ridge':
			p_vals = fitted_model.summary.pValues
			to_remove = []
			for i in range(len(featureCols)):
				if p_vals[i]>sig_level:
					to_remove.append(featureCols[i])
			#		print('---Insignificant feature! p = {:0.4f} - {}---'.format(p_vals[i], featureCols[i]))
			#print('Features with p_value > {} are discarded'.format(sig_level))
			#print('\n****************************************************************************************\n')
			significant_features = featureCols.copy()
			for item in to_remove:
				significant_features.remove(item)
			assembler = VectorAssembler(inputCols=significant_features, outputCol='features2')
			trainset = assembler.transform(trainset)
			testset = assembler.transform(testset)
			final_linear = SparkLinear(regParam=regParam, elasticNetParam=elasticNetParam, 
									featuresCol='features2', labelCol='RentalRate', predictionCol = 'RentalRate Prediction in SGD') 
			fitted_model = final_linear.fit(trainset)
	elif model_choice == 'RandomForest':
		numTrees = model_dict['NumTrees']
		maxDepth = model_dict['MaxDepth']
		feature_strat = model_dict['FeatureStrat']
		forest = SparkForest(labelCol='RentalRate',featuresCol='features',numTrees=numTrees, maxDepth=maxDepth, 
							maxMemoryInMB=1024, featureSubsetStrategy=feature_strat, predictionCol = 'RentalRate Prediction in SGD')
		fitted_model = forest.fit(trainset)
	elif model_choice == 'GBT':
		numTrees = model_dict['NumTrees']
		maxDepth = model_dict['MaxDepth']
		gbt = SparkGBT(labelCol='RentalRate',featuresCol='features',maxIter=numTrees, maxDepth=maxDepth, 
									  maxMemoryInMB=1024, predictionCol = 'RentalRate Prediction in SGD')
		fitted_model = gbt.fit(trainset)
	#print('Model is done being fitted!')
	#print('\n****************************************************************************************\n')
	return fitted_model, assembler, trainset, testset    
