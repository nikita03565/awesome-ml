import os
import pandas as pd
from pathlib import Path
from predictor.utils import lem, stem

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
parsed_dir = os.path.join(parent_dir, "data", "parsed")
result_dir = os.path.join(parent_dir, "data", "prepared")

def prepare():
    """
    This function uses parse data from csv, stemming texts and saves into csv file.
    """
    Path(result_dir).mkdir(exist_ok=True)
    df_parse_data = pd.read_csv(os.path.join(parsed_dir, "parsed.csv"))
    df_result = df_parse_data
    df_result["text_lem"] = df_result[~pd.isnull(df_result["text"])].apply(lambda row: lem(row["text"]), axis=1)
    df_result["text_stem"] = df_result[~pd.isnull(df_result["text"])].apply(lambda row: stem(row["text"]), axis=1)
    df_result.to_csv(os.path.join(result_dir, "prepared.csv"), encoding="utf-8", index=False)

if __name__ == "__main__":
    prepare()