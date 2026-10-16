import os 
from datetime import date

DB_NAME="Autism"
COLLECTION_NAME = "Autism_data"
CONNECTION_URL="mangoDB"

PIPLINE_NAME : str = "autism"
ARTIFACT_DIR: str = "artifact"
MODEL_FILE_NAME = "model.pkl"


DATA_INGESTION_COLLECTION_NAME: str = "Autism_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
FILE_NAME: str = "Autism.csv"
TRAIN_FILE_NAME: str = "train.csv"

TEST_FILE_NAME: str="test.csv"