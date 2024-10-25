import json

import boto3

endpoint_name = "my-model"
data = {"id": "434"}


sm_runtime = boto3.client("runtime.sagemaker", endpoint_url="http://localhost:4566")

response = sm_runtime.invoke_endpoint(
    EndpointName=endpoint_name, ContentType="application/json", Body=json.dumps(data)
)
response_str = response["Body"].read().decode()
response = json.loads(response_str)
print(response)
