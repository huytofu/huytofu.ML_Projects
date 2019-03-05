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