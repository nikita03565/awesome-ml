SHELL := /bin/bash

.PHONY: start-mlflow
start-mlflow:
	mkdir -p mlflow
	export MLFLOW_REGISTRY_URI=mlflow; \
	mlflow server --host localhost --port 5000 --backend-store-uri sqlite:///$$MLFLOW_REGISTRY_URI/mlflow.db --default-artifact-root $$MLFLOW_REGISTRY_URI


.PHONY: train
train:
	python predictor/train.py