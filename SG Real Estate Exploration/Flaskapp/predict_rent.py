from predict_test_instance import predict_test_instance
from create_prediction_model_sklearn import run_sklearn_session
from create_prediction_model_spark import run_spark_session

def run_rental_rate_prediction(choose_session, include_amen, amenities_list, regress_df_final, dict1, model_choice, model_dict):
	correct = False
	if choose_session == 'Sklearn':
		model, need_transformer, transformer, sample_predictions, r2_dict, rmse_dict=run_sklearn_session(regress_df_final, model_choice, model_dict)
		assembler = None
		sc = None
	else:
		model, assembler, sc, sample_predictions, r2_dict, rmse_dict=run_spark_session(regress_df_final, model_choice, model_dict)
		need_transformer = False
		transformer = None
	prediction = predict_test_instance(choose_session, include_amen, amenities_list, model, 
									need_transformer, transformer, assembler, sc, dict1, regress_df_final)
	return prediction, sample_predictions, r2_dict, rmse_dict

