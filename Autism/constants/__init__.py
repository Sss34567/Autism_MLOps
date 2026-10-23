import os 
from datetime import date

DB_NAME="Autism"
COLLECTION_NAME = "Autism_data"
CONNECTION_URL="mangoDB"

PIPLINE_NAME : str = "autism"
ARTIFACT_DIR: str = "artifact"
MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "Class/ASD"
CURRENT_YEAR = date.today().year
PREPROCSSING_OBJECT_FILE_NAME = "preprocssing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


AZURE_CONNECTION_STRING_ENV_KEY = "azureapi"
AZURE_CONTAINER_NAME = "models"
AZURE_MODEL_BLOB_NAME = "model.pkl"


DATA_INGESTION_COLLECTION_NAME: str = "Autism_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
FILE_NAME: str = "Autism.csv"
TRAIN_FILE_NAME: str = "train.csv"

TEST_FILE_NAME: str="test.csv"

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"



MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.80
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")


MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = AZURE_CONTAINER_NAME
MODEL_PUSHER_KEY = "model-registry"


APP_HOST = "127.0.0.1"
APP_PORT = 8080

