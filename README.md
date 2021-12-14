# Awesome ML project

To run backend create venv, install requirements and use commands:
```
cd backend
uvicorn main:app --reload
```


To start mlflow server use command:
```
make start-mlflow
```

Also create `confing.yaml` file in `predictor` directory using contents of `config_example.yaml` file. 
Change any values as you wish.

To train model use command:
```
make train
```
Note: `data` dir should be located in project root (for now).

To collect data use command:
```
make collect-data
```

To parse data use command:
```
make parse-data
```

To prepare (stem/lem) data use command:
```
make prepare-data
```

# Airflow setup
1. Run command:
```
pip install apache-airflow==2.0.1 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.0.1/constraints-3.7.txt"
```

2. Run command:
```
make setup-airflow
```

3. Open `airflow.cfg` and add/edit lines:
```
[webserver]
rbac = True
```
and
```
load_examples = False
dags_folder = ../dags
```

4. Run command
```
make create-airflow-user
```
5. And finally run commands in separate terminals:
```
make start-airflow
make start-airflow-scheduler
```
