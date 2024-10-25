#!/usr/bin/env python3
"""
File that Sagemaker reads to start the training, must be in the root folder
"""

from train.artifacts import (
    save_model,
    copy_inferance_file_to_model,
)


def fake_train():
    return {"id": "434"}


if __name__ == "__main__":
    # Fake Train
    model_dict = fake_train()

    # Save model artifacts
    save_model(model_dict)
    copy_inferance_file_to_model()

    print("Training finished!")
