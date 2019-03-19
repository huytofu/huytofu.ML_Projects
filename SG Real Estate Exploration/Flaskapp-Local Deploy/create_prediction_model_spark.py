import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression as SparkLinear 
from pyspark.ml.regression import GBTRegressor as SparkGBT
from pyspark.ml.regression import RandomForestRegressor as SparkForest
from pyspark.ml.evaluation import RegressionEvaluator

def run_spark_session(regress_df_final, model_choice, model_dict):

	def spark_create_datasets(sc, regress_df_final):
		data = sc.createDataFrame(regress_df_final)
		featureCols = data.columns
		featureCols.remove('Amenities')
		featureCols.remove('RentalRate')
		featureCols.remove('Description')
		featureCols.remove('ListingTitle')
		featureCols.remove('Url')
		assembler = VectorAssembler(inputCols=featureCols, outputCol='features')
		assembled = assembler.transform(data)
		trainset, testset = assembled.randomSplit([0.75,0.25], seed=0)
		return trainset, testset, featureCols, assembler

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
								maxMemoryInMB=2056, featureSubsetStrategy=feature_strat, predictionCol = 'RentalRate Prediction in SGD')
			fitted_model = forest.fit(trainset)
		elif model_choice == 'GBT':
			numTrees = model_dict['NumTrees']
			maxDepth = model_dict['MaxDepth']
			gbt = SparkGBT(labelCol='RentalRate',featuresCol='features',maxIter=numTrees, maxDepth=maxDepth, 
										  maxMemoryInMB=2056, predictionCol = 'RentalRate Prediction in SGD')
			fitted_model = gbt.fit(trainset)
		#print('Model is done being fitted!')
		#print('\n****************************************************************************************\n')
		return fitted_model, assembler, trainset, testset    

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

	def spark_collect_predictions(predictions_train, predictions_test):
		sample_predictions = dict()
		#print('Predictions for first 5 entries of trainset\n')
		answer_train = predictions_train.select(['ListingTitle', 'RentalRate', 'RentalRate Prediction in SGD']).take(5)
		sample_predictions['train'] = pd.DataFrame(data=answer_train, columns=['ListingTitle','True RentalRate','RentalRate Prediction in SGD'])
		#print('Prediction for firest 5 entries of testset\n')
		answer_test = predictions_test.select(['ListingTitle', 'RentalRate', 'RentalRate Prediction in SGD']).take(5)
		sample_predictions['test'] = pd.DataFrame(data=answer_test, columns=['ListingTitle','True RentalRate','RentalRate Prediction in SGD'])
		return sample_predictions

	sc = SparkSession.builder.appName('Huy').getOrCreate()
	trainset, testset, featureCols, assembler = spark_create_datasets(sc, regress_df_final)
	model, assembler, trainset, testset = spark_create_model(trainset, testset, featureCols, assembler, model_choice, model_dict)
	predictions_train, predictions_test, r2_dict, rmse_dict = spark_evaluate_results(model, trainset, testset)
	sample_predictions = spark_collect_predictions(predictions_train, predictions_test)
	return model, assembler, sc, sample_predictions, r2_dict, rmse_dict