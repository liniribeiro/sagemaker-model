import boto3

from tools.sagemaker.update_endpoint import (
    create_sagemaker_model,
    update_endpoint_new_model,
)
from settings import EXECUTION_ROLE, S3_BUCKET_NAME

import time


sagemaker_client = boto3.client(
    "sagemaker", endpoint_url="http://localhost:4566"
)

s3_train_dir = f"s3://{S3_BUCKET_NAME}/training/code/train.tar.gz"
output_path = f"s3://{S3_BUCKET_NAME}/training"
instance_type = "ml.m5.4xlarge"
image_uri = (
    "aliniribeiroo/sagemaker-model:dev"
)

# Names must be unique
time = time.strftime("%Y-%m-%d-%H-%M-%S")
name = f"model{time}"

hyperparameters = {}
environment_variables = {
    "ENVIRONMENT": "staging",
}
ecr_container_url = image_uri
sagemaker_role = "arn:aws:iam::000000000000:policy/train-job]"

output_bucket = output_path
instance_count = 1
memory_volume = 8


def start_training():
    _ = sagemaker_client.create_training_job(
        TrainingJobName=name,
        HyperParameters=hyperparameters,
        AlgorithmSpecification={
            "TrainingImage": ecr_container_url,
            "TrainingInputMode": "File",
            "ContainerEntrypoint": ["train/start.py"],
        },
        RoleArn=sagemaker_role,
        OutputDataConfig={"S3OutputPath": output_bucket},
        ResourceConfig={
            "InstanceType": instance_type,
            "InstanceCount": instance_count,
            "VolumeSizeInGB": memory_volume,
        },
        Environment=environment_variables,
        StoppingCondition={"MaxRuntimeInSeconds": 43200},
    )


def wait_training_finish(training_job_name):
    """
    While the endpoint is being created or updated sleep for 60 seconds.
    """
    waiter = sagemaker_client.get_waiter("training_job_completed_or_stopped")

    waiter.wait(TrainingJobName=name, WaiterConfig={"Delay": 35, "MaxAttempts": 123})

    training_job = sagemaker_client.describe_training_job(
        TrainingJobName=training_job_name
    )
    _training_status = training_job["TrainingJobStatus"]
    _execution_time = training_job["TrainingTimeInSeconds"]
    model_path = training_job["ModelArtifacts"]["S3ModelArtifacts"]
    return model_path


start_training()

model_path = wait_training_finish(name)

create_sagemaker_model(model_url=model_path, model_name=name)

endpoint_name = "endpoint-name"
update_endpoint_new_model(name, endpoint_name)
