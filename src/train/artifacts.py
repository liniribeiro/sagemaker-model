import json
import os
import shutil

from settings import (
    MODEL_OUTPUT_PATH,
    INFERENCE_DIR,
)


def copy_inferance_file_to_model():
    # Save inferance file into the model (Used for the sagemaker /invocation)
    inferance_code_path = os.path.join(MODEL_OUTPUT_PATH, "code", "inference.py")
    print(os.listdir())
    if not os.path.exists(inferance_code_path):
        os.makedirs(os.path.dirname(inferance_code_path), exist_ok=True)
    shutil.copy(os.path.join(INFERENCE_DIR, "inference.py"), inferance_code_path)


def save_model(data: dict):
    file_path = f"{MODEL_OUTPUT_PATH}/model.json"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    print(f"Saving model at: {file_path}")
    with open(file_path, "w") as file:
        file.write(json.dumps(data))

