# Sagemaker Inference file


With Amazon SageMaker, you can start getting predictions, or inferences, from your trained machine learning models.
SageMaker provides a broad selection of ML infrastructure and model deployment options to help meet all our ML inference needs.
With SageMaker Inference, we can scale our model deployment, manage models more effectively in production, and reduce operational burden.

SageMaker provides us various inference options, such as real-time endpoints for getting low latency inference,
serverless endpoints for fully managed infrastructure and auto-scaling, and asynchronous endpoints for batches of requests.
By leveraging the appropriate inference option for our use case, we can ensure efficient and model deployment and inference.

## How this works

Every time that we train the model, the inference.py is packed too, inside code/inference.py.
This model is deployed to sagemaker, a new configuration is created and when we are updating our endpoint with the new config,
it will try to find the inference.py file inside our model, then make the endpoint available.

This is a simple solution for the spike, if we see that we need to add more complexity into the model inference,
we can evolve to maybe build an image for it, this is not necessary right now, because the endpoint just serve us the model.