import sys
from typing import Tuple

from sklearn.metrics import f1_score, precision_score, recall_score
from neuro_mf import ModelFactory

from Autism.exception import AutismException
from Autism.logger import logging
from Autism.utils.main_utils import load_numpy_array_data, load_object, save_object
from Autism.entity.config_entity import ModelTrainerConfig
from Autism.entity.artifact_entity import (
    DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact)
from Autism.entity.estimator import AutismModel

THRESHOLD = 0.30


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train, test) -> Tuple[object, object]:
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            x_train, y_train = train[:, :-1], train[:, -1].astype(int)
            x_test, y_test = test[:, :-1], test[:, -1].astype(int)

            best_model_detail = model_factory.get_best_model(
                X=x_train, y=y_train,
                base_accuracy=self.model_trainer_config.expected_accuracy)
            model_obj = best_model_detail.best_model

            y_proba = model_obj.predict_proba(x_test)[:, 1]
            y_pred = (y_proba >= THRESHOLD).astype(int)

            metric_artifact = ClassificationMetricArtifact(
                f1_score=f1_score(y_test, y_pred),
                precision_score=precision_score(y_test, y_pred),
                recall_score=recall_score(y_test, y_pred))
            return best_model_detail, metric_artifact
        except Exception as e:
            raise AutismException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            preprocessing_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                raise Exception("No best model found with score more than base score")

            autism_model = AutismModel(preprocessing_object=preprocessing_obj,
                                       trained_model_object=best_model_detail.best_model,
                                       threshold=THRESHOLD)
            save_object(self.model_trainer_config.trained_model_file_path, autism_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise AutismException(e, sys) from e
