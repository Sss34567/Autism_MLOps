import sys
from pandas import DataFrame

from Autism.entity.config_entity import AutismPredictorConfig
from Autism.entity.azure_estimator import AutismEstimator
from Autism.exception import AutismException
from Autism.logger import logging


class AutismData:
    def __init__(self, A1_Score, A2_Score, A3_Score, A4_Score, A5_Score,
                 A6_Score, A7_Score, A8_Score, A9_Score, A10_Score,
                 age, ethnicity, jaundice, austim, contry_of_res):
        try:
            self.scores = [A1_Score, A2_Score, A3_Score, A4_Score, A5_Score,
                           A6_Score, A7_Score, A8_Score, A9_Score, A10_Score]
            self.age = age
            self.ethnicity = ethnicity
            self.jaundice = jaundice
            self.austim = austim
            self.contry_of_res = contry_of_res
        except Exception as e:
            raise AutismException(e, sys) from e

    def get_autism_data_as_dict(self) -> dict:
        try:
            input_data = {f"A{i+1}_Score": [int(s)] for i, s in enumerate(self.scores)}
            input_data.update({
                "age": [float(self.age)],
                "ethnicity": [self.ethnicity],
                "jaundice": [self.jaundice],
                "austim": [self.austim],
                "contry_of_res": [self.contry_of_res],
                "result": [sum(int(s) for s in self.scores)],  # مجموع الإجابات
            })
            return input_data
        except Exception as e:
            raise AutismException(e, sys) from e

    def get_autism_input_data_frame(self) -> DataFrame:
        try:
            return DataFrame(self.get_autism_data_as_dict())
        except Exception as e:
            raise AutismException(e, sys) from e


class AutismClassifier:
    def __init__(self, prediction_pipeline_config: AutismPredictorConfig = AutismPredictorConfig()) -> None:
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise AutismException(e, sys)

    def predict(self, dataframe):
        try:
            logging.info("Entered predict method of AutismClassifier class")
            model = AutismEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            return model.predict(dataframe)
        except Exception as e:
            raise AutismException(e, sys)
