from settings import EXECUTION_ROLE

import boto3
import time


# name of zipped model and zipped inference code
INSTANCE_TYPE = "ml.m5.4xlarge"
# sagemaker params
sagemaker_client = boto3.client("sagemaker", endpoint_url="http://localhost:4566")


def deploy_new_endpoint(model_name):
    print("Deploying for the first time")

    endpoint_config_name = model_name
    endpoint_name = model_name

    # here you should copy and zip the model dependencies that you may have (such as preprocessors, inference code, config code...)
    # mine were zipped into the file called CODE_TAR

    # create sagemaker model and endpoint configuration
    create_sagemaker_model(model_name=model_name)
    create_endpoint_config(model_name)

    # deploy model and wait while endpoint is being created
    create_endpoint(endpoint_name, endpoint_config_name)
    wait_while_creating(endpoint_name)


def update_endpoint_new_model(new_model_name, endpoint_name):
    """
    Main method to create a sagemaker model, create an endpoint configuration and deploy the model. If deployRetrained
    param is set to True, this method will update an already existing endpoint.
    """
    # define model name and endpoint name to be used for model deployment/update
    endpoint_config_name = new_model_name

    outdated_endpoint_config_name = sagemaker_client.describe_endpoint(
        EndpointName=endpoint_name
    )["EndpointConfigName"]

    print("Updating existing model")

    # create a new endpoint config that takes the new model
    create_endpoint_config(new_model_name)

    # update endpoint
    update_endpoint(endpoint_name, endpoint_config_name)

    # wait while endpoint updates then delete outdated endpoint config once it is InService
    wait_while_creating(endpoint_name)
    delete_outdated_endpoint_config(outdated_endpoint_config_name)


def create_sagemaker_model(model_url, model_name):
    """
    Create a new sagemaker Model object with an pytorch container and an entry point for inference using boto3 API
    """
    # Retrieve that inference image (container)
    image_uri = (
        "763104351884.dkr.ecr.us-east-1.amazonaws.com/pytorch-inference:1.3-cpu-py3"
    )

    # Create a sagemaker Model object with all its artifacts
    sagemaker_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=EXECUTION_ROLE,
        PrimaryContainer={
            "Image": image_uri,
            "ModelDataUrl": model_url,
            "Environment": {
                "SAGEMAKER_PROGRAM": "inference.py",
                "SAGEMAKER_REGION": "us-east-1",
                "SAGEMAKER_SUBMIT_DIRECTORY": "/opt/ml/model/code",
            },
        },
    )


def create_endpoint_config(model_name):
    """
    Create an endpoint configuration (only for boto3 sdk procedure) and set production variants parameters.
    Each retraining procedure will induce a new variant name based on the endpoint configuration name.
    At this example we are just using one variant, but in the future we can add more variants (trained models) and apply weights
    """
    endpoint_config_name = model_name
    sagemaker_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "VariantName": endpoint_config_name,
                "ModelName": model_name,
                "InstanceType": INSTANCE_TYPE,
                "InitialInstanceCount": 1,
            }
        ],
    )


def create_endpoint(endpoint_name, endpoint_config_name):
    """
    Deploy the model to an endpoint
    """
    sagemaker_client.create_endpoint(
        EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
    )


def delete_outdated_endpoint_config(outdated_endpoint_config_name):
    """
    Delete outdated endpoint config and model, Every time that a new train happen, a new endpoint and model are created
    We dont need to store the old endpoints or models, because we already have the generated model from the training notebook at our stats bucket
    Even if we delete a config that was used to update an endpoint, nothing happens with the endpoint, it stll will be running without problems.
    """
    sagemaker_client.delete_endpoint_config(
        EndpointConfigName=outdated_endpoint_config_name
    )

    sagemaker_client.delete_model(ModelName=outdated_endpoint_config_name)


def update_endpoint(endpoint_name, endpoint_config_name):
    """
    Update existing endpoint with a new retrained model
    """
    sagemaker_client.update_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name,
        RetainAllVariantProperties=True,
    )


def wait_while_creating(endpoint_name):
    """
    While the endpoint is being created or updated sleep for 60 seconds.
    """
    # wait while creating or updating endpoint
    status = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)[
        "EndpointStatus"
    ]
    print("Status: %s" % status)
    while status != "InService" and status != "Failed":
        time.sleep(60)
        status = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)[
            "EndpointStatus"
        ]
        print("Status: %s" % status)

    # in case of a deployment failure raise an error
    if status == "Failed":
        raise ValueError("Endpoint failed to deploy")
