import os

import mlflow
import pandas as pd
import yaml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split

from predictor.utils import get_production_model_version

# dirty file for testing purpose
# contains example of model loading

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(parent_dir, "predictor", "config.yaml")

config = yaml.safe_load(open(config_path))
mlflow_root = "mlflow"


if __name__ == "__main__":
    mlflow.set_tracking_uri(config["global"]["mlflow_uri"])
    model_name = config["train"]["model_name"]
    latest_version = get_production_model_version(config["train"]["model_name"]) or config["predict"]["version"]

    model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{latest_version}")

    #####
    filename = os.path.join("data", "prepared", "prepared.csv")
    df = pd.read_csv(filename, nrows=1000)
    df_lem = df[["text_lem", "rating"]].dropna()
    X, y = df_lem["text_lem"], df_lem["rating"]
    tfidfconverter = TfidfTransformer()
    vectorizer = CountVectorizer(max_features=1000, min_df=5, max_df=0.7)
    X_countVectorizer = vectorizer.fit_transform(X).toarray()
    X_tfIdf = tfidfconverter.fit_transform(X_countVectorizer).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X_tfIdf, y, test_size=0.2, random_state=0)
    #####

    print(model)
    print(model.predict(X_test))
