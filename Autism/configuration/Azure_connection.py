import os
from azure.storage.blob import BlobServiceClient
from Autism.constants import AZURE_CONNECTION_STRING_ENV_KEY


class AzureClient:
    blob_service_client = None

    def __init__(self):
        if AzureClient.blob_service_client is None:
            conn = os.getenv(AZURE_CONNECTION_STRING_ENV_KEY)
            if conn is None:
                raise Exception(f"Environment variable {AZURE_CONNECTION_STRING_ENV_KEY} is not set")
            AzureClient.blob_service_client = BlobServiceClient.from_connection_string(conn)
        self.blob_service_client = AzureClient.blob_service_client
