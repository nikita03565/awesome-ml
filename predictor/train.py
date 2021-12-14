import os

import mlflow
import pandas as pd
import yaml
import json
from catboost import CatBoostRegressor

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from predictor.utils import get_version_model

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(parent_dir, "predictor", "config.yaml")

local_path = os.path.join(parent_dir, "predictor", "train.py")
vocabulary_path = os.path.join(parent_dir, "predictor", "vocabulary.json")

config = yaml.safe_load(open(config_path))["train"]
global_config = yaml.safe_load(open(config_path))["global"]

count_vect_params = config["count_vect_params"]
catboost_params = config["catboost_params"]

regression_artifact_path = "regression"

def save_vocabulary(vocabulary: dict):
    new = vocabulary

    for k in vocabulary:
        new[k] = int(vocabulary[k])

    with open(vocabulary_path, "w") as f:
        f.write(json.dumps(new, ensure_ascii=False))

def train(filename=os.path.join(parent_dir, "data", "prepared", "prepared.csv")):
    df = pd.read_csv(filename)
    df_stem = df[["text_stem", "rating"]].dropna()
    X, y = df_stem["text_stem"], df_stem["rating"]

    tfidfconverter = TfidfTransformer()
    vectorizer = CountVectorizer(max_features=count_vect_params['max_features'], min_df=count_vect_params['min_df'], max_df=count_vect_params['max_df'])
    X_countVectorizer = vectorizer.fit_transform(X).toarray()
    save_vocabulary(vectorizer.vocabulary_)
    X_tfIdf = tfidfconverter.fit_transform(X_countVectorizer).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X_tfIdf, y, test_size=0.2, random_state=0)

    run_id = ''

    mlflow.set_tracking_uri(global_config["mlflow_uri"])
    mlflow.set_experiment(config["experiment_name"])

    experiment_id = mlflow.get_experiment_by_name(config["experiment_name"]).experiment_id

    with mlflow.start_run() as train_run:
        run_id = train_run.info.run_id
        reg = CatBoostRegressor(iterations=catboost_params['iterations'], learning_rate=catboost_params['learning_rate'], depth=catboost_params['depth'], verbose=catboost_params['verbose']).fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(reg, artifact_path=regression_artifact_path, registered_model_name=config["model_name"])

        mlflow.log_artifact(local_path=local_path, artifact_path="code")
        mlflow.end_run()

    last_model_version = get_version_model(config["model_name"])

    yaml_file = yaml.safe_load(open(config_path))
    yaml_file["predict"]["version"] = int(last_model_version)
    yaml_file["predict"]["model_path"] = os.path.join(parent_dir, "mlflow", experiment_id, run_id, "artifacts", regression_artifact_path)

    with open(config_path, "w") as fp:
        yaml.dump(yaml_file, fp, encoding="UTF-8", allow_unicode=True)


if __name__ == "__main__":
    train()
