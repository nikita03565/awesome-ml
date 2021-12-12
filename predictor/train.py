import os

import mlflow
import pandas as pd
import yaml
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

config = yaml.safe_load(open(config_path))["train"]
global_config = yaml.safe_load(open(config_path))["global"]
params_config = yaml.safe_load(open(config_path))["params"]


def train(filename=os.path.join(parent_dir, "data", "prepared", "prepared.csv")):
    df = pd.read_csv(filename)
    df_stem = df[["text_stem", "rating"]].dropna()
    X, y = df_stem["text_stem"], df_stem["rating"]

    tfidfconverter = TfidfTransformer()
    vectorizer = CountVectorizer(max_features=params_config['max_features'], min_df=params_config['min_df'], max_df=params_config['max_df'])
    X_countVectorizer = vectorizer.fit_transform(X).toarray()
    X_tfIdf = tfidfconverter.fit_transform(X_countVectorizer).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X_tfIdf, y, test_size=0.2, random_state=0)

    mlflow.set_tracking_uri(global_config["mlflow_uri"])
    mlflow.set_experiment(config["experiment_name"])
    with mlflow.start_run():
        reg = CatBoostRegressor(iterations=params_config['iterations'], learning_rate=params_config['learning_rate'], depth=params_config['depth'], verbose=params_config['verbose']).fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        # Log any metrics you want here
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        # Log the model itself
        mlflow.sklearn.log_model(reg, artifact_path="regression", registered_model_name=config["model_name"])
        # And code that's been used to create model
        mlflow.log_artifact(local_path=local_path, artifact_path="code")
        mlflow.end_run()

    last_model_version = get_version_model(config["model_name"])

    yaml_file = yaml.safe_load(open(config_path))
    yaml_file["predict"]["version"] = int(last_model_version)

    with open(config_path, "w") as fp:
        yaml.dump(yaml_file, fp, encoding="UTF-8", allow_unicode=True)


if __name__ == "__main__":
    train()
