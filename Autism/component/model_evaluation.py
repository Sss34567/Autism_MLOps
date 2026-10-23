import sys
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sklearn.metrics import recall_score

from Autism.entity.config_entity import ModelEvaluationConfig
from Autism.entity.artifact_entity import (
    ModelTrainerArtifact,
    DataIngestionArtifact,
    ModelEvaluationArtifact,
)
from Autism.entity.azure_estimator import AutismEstimator
from Autism.exception import AutismException
from Autism.logger import logging
from Autism.constants import TARGET_COLUMN


@dataclass
class EvaluateModelResponse:
    trained_model_recall_score: float
    best_model_recall_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:
    def __init__(self, model_eval_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise AutismException(e, sys) from e

    def get_best_model(self) -> Optional[AutismEstimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.model_key_path
            autism_estimator = AutismEstimator(bucket_name=bucket_name,
                                               model_path=model_path)
            if autism_estimator.is_model_present(model_path=model_path):
                return autism_estimator
            return None
        except Exception as e:
            raise AutismException(e, sys) from e

    def evaluate_model(self) -> EvaluateModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            x = test_df.drop(TARGET_COLUMN, axis=1)
            y = test_df[TARGET_COLUMN].astype(int)

            trained_model_recall_score = self.model_trainer_artifact.metric_artifact.recall_score

            best_model_recall_score = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(x)
                best_model_recall_score = recall_score(y, y_hat_best_model)

            tmp_best_model_score = 0 if best_model_recall_score is None else best_model_recall_score

            result = EvaluateModelResponse(
                trained_model_recall_score=trained_model_recall_score,
                best_model_recall_score=best_model_recall_score,
                is_model_accepted=trained_model_recall_score > tmp_best_model_score + self.model_eval_config.changed_threshold_score,
                difference=trained_model_recall_score - tmp_best_model_score,
            )
            logging.info(f"Result: {result}")
            return result
        except Exception as e:
            raise AutismException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            evaluate_model_response = self.evaluate_model()
            model_path = self.model_eval_config.model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                model_path=model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference,
            )
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise AutismException(e, sys) from e
