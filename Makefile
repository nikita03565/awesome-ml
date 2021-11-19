SHELL := /bin/bash

.PHONY: start-mlflow
start-mlflow:
	mkdir -p mlflow
	export MLFLOW_REGISTRY_URI=mlflow; \
	mlflow server --host localhost --port 5000 --backend-store-uri sqlite:///$$MLFLOW_REGISTRY_URI/mlflow.db --default-artifact-root $$MLFLOW_REGISTRY_URI

.PHONY: setup-airflow
setup-airflow:
	mkdir -p airflow; \
	cd airflow; \
	export AIRFLOW_HOME=.; \
	airflow db init;

.PHONY: create-airflow-user
create-airflow-user:
	cd airflow; \
	export AIRFLOW_HOME=.; \
	airflow users create --username user --firstname user --lastname user --role Admin --email user@test.com

.PHONY: start-airflow
start-airflow:
	cd airflow; \
	export AIRFLOW_HOME=.; \
	airflow webserver -p 8080; \

.PHONY: start-airflow-scheduler
start-airflow-scheduler:
	cd airflow; \
	export AIRFLOW_HOME=.; \
	airflow scheduler; \

.PHONY: train
train:
	PYTHONPATH=. python predictor/train.py

.PHONY: test-predict
test-predict:
	PYTHONPATH=. python predictor/test_predict.py

.PHONY: collect-data
collect-data:
	PYTHONPATH=. python scraper/main.py

.PHONY: parse-data
parse-data:
	PYTHONPATH=. python scraper/parse.py
