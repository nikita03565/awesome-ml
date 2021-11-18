import os

import mlflow
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

DATA_DIR = "data"


def get_version_model(config_name, client):
    """
    Gets latest versions of model
    """
    dict_push = {}
    for count, value in enumerate(client.search_model_versions(f"name='{config_name}'")):
        dict_push[count] = value
    return dict(list(dict_push.items())[-1][1])["version"]


def train(filename=os.path.join(DATA_DIR, "data.csv")):
    df = pd.read_csv(filename, nrows=50000)
    df_lem = df[["text_lem", "rating"]].dropna()
    X, y = df_lem["text_lem"], df_lem["rating"]
    tfidfconverter = TfidfTransformer()
    vectorizer = CountVectorizer(max_features=1000, min_df=5, max_df=0.7)
    X_countVectorizer = vectorizer.fit_transform(X).toarray()
    X_tfIdf = tfidfconverter.fit_transform(X_countVectorizer).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X_tfIdf, y, test_size=0.2, random_state=0)

    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("test")
    with mlflow.start_run():
        reg = LinearRegression().fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        # Log any metrics you want here
        mlflow.log_param("mse", mse)
        # Log the model itself
        mlflow.sklearn.log_model(reg, artifact_path="regression", registered_model_name=f"test_model")
        # And code that's been used to create model
        mlflow.log_artifact(local_path="predictor/train.py", artifact_path="code")
        mlflow.end_run()


if __name__ == "__main__":
    train()
