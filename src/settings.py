import os


ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INFERENCE_DIR = f"{BASE_DIR}/inference/"
S3_BUCKET_NAME = f"bucket-{ENVIRONMENT}"

EXECUTION_ROLE = os.getenv(
    "SAGEMAKER_EXECUTION_ROLE",
    "xxx",
)


# STANDART SAGEMAKER PATH
SAGEMAKER_PATH = "/opt/ml"

# Path were sagemaker will search for artefacts to send to S3 output folder
MODEL_OUTPUT_PATH = os.getenv("MODEL_OUTPUT_PATH", f"{SAGEMAKER_PATH}/model")


