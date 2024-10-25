import json
import os


def model_fn(model_dir):
    """
    function will deserialize your machine learning model
    """
    file_path = os.path.join(model_dir, "model.json")
    with open(file_path, mode="rb") as fp:
        model = json.load(fp)
    return model


def input_fn(request_body, content_type="application/json"):
    if content_type == "application/json":
        input_data = json.loads(request_body)
        model_id = input_data.get("id", None)
        return model_id


def predict_fn(input_data, model):
    if input_data:
        return model[input_data]
    else:
        return model


def output_fn(prediction, content_type):
    return json.dumps(prediction)
