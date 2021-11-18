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

To train model use command:
```
make train
```
Note: `data` dir should be located in project root (for now).