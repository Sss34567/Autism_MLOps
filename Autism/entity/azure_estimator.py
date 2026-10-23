import sys
from pandas import DataFrame

from Autism.Cloud_storage.Azure_storage import SimpleStorageService
from Autism.exception import AutismException
from Autism.entity.estimator import AutismModel


class AutismEstimator:
    """Save and retrieve the autism model in Azure Blob Storage and do prediction."""

    def __init__(self, bucket_name: str, model_path: str):
        
        self.bucket_name = bucket_name
        self.azure = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: AutismModel = None

    def is_model_present(self, model_path: str) -> bool:
        try:
            return self.azure.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except AutismException as e:
            print(e)
            return False

    def load_model(self) -> AutismModel:
        return self.azure.load_model(self.model_path, bucket_name=self.bucket_name)

    def save_model(self, from_file: str, remove: bool = False) -> None:
        try:
            self.azure.upload_file(from_file,
                                   to_filename=self.model_path,
                                   bucket_name=self.bucket_name,
                                   remove=remove)
        except Exception as e:
            raise AutismException(e, sys)

    def predict(self, dataframe: DataFrame):
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise AutismException(e, sys)
