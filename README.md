Directory Structure

[Inspired in cookiecutter](https://cookiecutter-data-science.drivendata.org/#directory-structure)

```
── sagemaker-model <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes the folder a Python module
    │
    ├── settings.py             <- Store useful variables and configuration
    │
    ├── tools                   <- Tools used for dev when developing new features
    │   │
    │   ├── build.sh
    │   └── ..
    ├── src                     <- All the code that will be packed
    │   │
    │   ├── settings.py         <- Shared settings between train and predict
    │   ├── train               <- Code to train models
    │   │   │
    │   │   ├── __init__.py
    │   │   └── ...
    │   ├── inference           <- Code to run model inference with trained models
    │   │   │
    │   │   ├── __init__.py
    │   │   └── ...
    │
    └── Dockerfile              <- The recipe to build the train and predict images

```


## [Sagemaker Channels](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_Channel.html)
Sagemaker channels kinda are input that we add to our training.

Sagemaker will pré-load the channel data into our container when the training starts, that´s why we must follow a certain folder structure when building the training image.
At this project, we will find our channel giles in the path:
- "opt/ml/input/data/model": for the model
When running the service locally, the default folder is /data (you can look for our docker-compose that has its an example, we mount the local data/ folder to simulate the container folder structure)

## [Output Model]
After the training and generating our important files, we should save everything under the directory "opt/ml/model".
Sagemaker will pack everything that is under this directory and store it as model.tar.gz.
This model then can be used to deploy new sagemaker endpoints,


Folder structured used by the model (sagemaker):
/opt/ml
|-- input
|   |-- config
|   |   |-- hyperparameters.json
|   |   `-- resourceConfig.json
|   `-- data
|       `-- <channel_name>
|           `-- <input data>
|-- model
|   `-- <model files> ------> HERE


## Updating Requirements


The `requirements[-dev].txt` files are generated using [uv](https://github.com/astral-sh/uv).

```bash
# Install uv tool
brew install uv
```
```bash
# Generates requirements.txt
uv pip compile --python python3.11 src/requirements/base.in -o src/requirements.txt

# Generates requirements-dev.txt
uv pip compile --python python3.11 src/requirements/dev.in -o src/requirements-dev.txt

```

# Running the training locally:

- run script tools/load_data_files_for_local_training.sh -> this will download the datasets files and create the apropriate directories to store the trained model.

[Joblib](https://joblib.readthedocs.io/en/stable/)
[Dockerhub image repo](https://hub.docker.com/r/aliniribeiroo/sagemaker-model/tags)