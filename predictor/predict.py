import os

import mlflow
import yaml
import json
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from predictor.utils import stem, get_version_model, get_production_model_version

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(parent_dir, "predictor", "config.yaml")
vocabulary_path = os.path.join(parent_dir, "predictor", "vocabulary.json")

config_path = config = yaml.safe_load(open(config_path))
global_config = config_path["global"]
config = config_path["train"]
predict_config = config_path["predict"]

count_vect_params = config["count_vect_params"]
catboost_params = config["catboost_params"]

def get_prediction(article_text: str):
    stem_text = pd.Series(data=stem(article_text))
    tfidfconverter = TfidfTransformer()
    with open(vocabulary_path, "r") as f:
        vocabulary = json.loads(f.read())

        vectorizer = CountVectorizer(vocabulary=vocabulary, max_features=count_vect_params['max_features'])
        X_countVectorizer = vectorizer.fit_transform(stem_text).toarray()
        X_tfIdf = tfidfconverter.fit_transform(X_countVectorizer)
        
        mlflow.set_tracking_uri(global_config["mlflow_uri"])

        model_name = config["model_name"]
        latest_version = get_production_model_version(config["model_name"]) or predict_config["version"]

        print("set_tracking_uri ", global_config["mlflow_uri"])
        print("model_name ", model_name)
        print("latest_version ", latest_version)
    
        # не хочет работать 
        loaded_model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{latest_version}")

        # работает
        # loaded_model = mlflow.pyfunc.load_model(model_uri=os.path.join(parent_dir, "mlflow", "1", "1d847a48016e4392943c6cb48e0418ab", "artifacts", "regression"))
        test_predictions = loaded_model.predict(X_tfIdf)
        # mlflow.log_param("test_predictions", test_predictions)

        return test_predictions[0]

if __name__ == "__main__":
    print(get_prediction("Вот тогда мы и использовали стикеры, чтоб не дай боже глянуть. Кстати, она оказалась, в отличие от обычных высокомерных "))
