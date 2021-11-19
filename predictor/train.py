import os

import mlflow
import pandas as pd
import yaml

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from predictor.utils import get_version_model

DATA_DIR = "data"
config_path = os.path.join("predictor", "config.yaml")

config = yaml.safe_load(open(config_path))["train"]
global_config = yaml.safe_load(open(config_path))["global"]


def train(filename=os.path.join(DATA_DIR, "data.csv")):
    df = pd.read_csv(filename, nrows=1000)
    df_lem = df[["text_lem", "rating"]].dropna()
    X, y = df_lem["text_lem"], df_lem["rating"]
    tfidfconverter = TfidfTransformer()
    vectorizer = CountVectorizer(max_features=1000, min_df=5, max_df=0.7)
    X_countVectorizer = vectorizer.fit_transform(X).toarray()
    X_tfIdf = tfidfconverter.fit_transform(X_countVectorizer).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X_tfIdf, y, test_size=0.2, random_state=0)

    mlflow.set_tracking_uri(global_config["mlflow_uri"])
    mlflow.set_experiment(config["experiment_name"])
    with mlflow.start_run():
        reg = LinearRegression().fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        # Log any metrics you want here
        mlflow.log_param("mse", mse)
        # Log the model itself
        mlflow.sklearn.log_model(reg, artifact_path="regression", registered_model_name=config["model_name"])
        # And code that's been used to create model
        mlflow.log_artifact(local_path="predictor/train.py", artifact_path="code")
        mlflow.end_run()

    last_model_version = get_version_model(config["model_name"])

    yaml_file = yaml.safe_load(open(config_path))
    yaml_file["predict"]["version"] = int(last_model_version)

    with open(config_path, "w") as fp:
        yaml.dump(yaml_file, fp, encoding="UTF-8", allow_unicode=True)


if __name__ == "__main__":
    train()
