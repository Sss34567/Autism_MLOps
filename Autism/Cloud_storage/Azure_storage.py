import os
import sys
from io import StringIO
from typing import Union

import dill
from azure.storage.blob import ContainerClient, BlobClient
from pandas import DataFrame, read_csv

from Autism.configuration.Azure_connection import AzureClient
from Autism.exception import AutismException
from Autism.logger import logging


class SimpleStorageService:

    def __init__(self):
        self.blob_service_client = AzureClient().blob_service_client

    def get_bucket(self, bucket_name: str) -> ContainerClient:
        try:
            return self.blob_service_client.get_container_client(bucket_name)
        except Exception as e:
            raise AutismException(e, sys) from e

    def s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        try:
            container = self.get_bucket(bucket_name)
            return any(True for _ in container.list_blobs(name_starts_with=s3_key))
        except Exception as e:
            raise AutismException(e, sys)

    @staticmethod
    def read_object(object_name: BlobClient, decode: bool = True,
                    make_readable: bool = False) -> Union[StringIO, str, bytes]:
        try:
            data = object_name.download_blob().readall()
            if decode:
                data = data.decode()
            return StringIO(data) if make_readable else data
        except Exception as e:
            raise AutismException(e, sys) from e

    def get_file_object(self, filename: str, bucket_name: str) -> BlobClient:
        try:
            return self.get_bucket(bucket_name).get_blob_client(filename)
        except Exception as e:
            raise AutismException(e, sys) from e

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        try:
            model_file = model_name if model_dir is None else model_dir + "/" + model_name
            blob = self.get_file_object(model_file, bucket_name)
            model_bytes = self.read_object(blob, decode=False)
            return dill.loads(model_bytes)
        except Exception as e:
            raise AutismException(e, sys) from e

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        try:
            blob = self.get_file_object(folder_name + "/", bucket_name)
            if not blob.exists():
                blob.upload_blob(b"")
        except Exception as e:
            raise AutismException(e, sys) from e

    def upload_file(self, from_filename: str, to_filename: str,
                    bucket_name: str, remove: bool = True):
        try:
            logging.info(f"Uploading {from_filename} to {to_filename} in {bucket_name} container")
            container = self.get_bucket(bucket_name)
            with open(from_filename, "rb") as f:
                container.upload_blob(name=to_filename, data=f, overwrite=True)
            logging.info(f"Uploaded {from_filename} to {to_filename} in {bucket_name} container")
            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")
        except Exception as e:
            raise AutismException(e, sys) from e

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str,
                         bucket_filename: str, bucket_name: str) -> None:
        try:
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise AutismException(e, sys) from e

    def get_df_from_object(self, object_: BlobClient) -> DataFrame:
        try:
            content = self.read_object(object_, make_readable=True)
            return read_csv(content, na_values="na")
        except Exception as e:
            raise AutismException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        try:
            blob = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(blob)
        except Exception as e:
            raise AutismException(e, sys) from e
