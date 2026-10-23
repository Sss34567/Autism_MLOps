import sys

from Autism.Cloud_storage.Azure_storage import SimpleStorageService
from Autism.exception import AutismException
from Autism.logger import logging
from Autism.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from Autism.entity.config_entity import ModelPusherConfig
from Autism.entity.azure_estimator import AutismEstimator


class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        try:
            self.s3 = SimpleStorageService()
            self.model_evaluation_artifact = model_evaluation_artifact
            self.model_pusher_config = model_pusher_config
            self.autism_estimator = AutismEstimator(
                bucket_name=model_pusher_config.bucket_name,
                model_path=model_pusher_config.model_key_path,
            )
        except Exception as e:
            raise AutismException(e, sys) from e

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            logging.info("Uploading model to Azure container")

            self.autism_estimator.save_model(
                from_file=self.model_evaluation_artifact.trained_model_path
            )

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                model_path=self.model_pusher_config.model_key_path,
            )

            logging.info("Uploaded model to Azure container")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            return model_pusher_artifact
        except Exception as e:
            raise AutismException(e, sys) from e
