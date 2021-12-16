import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'email': ['user@test.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
        'full-work',
        default_args=default_args,
        description='Collects, Parse, Prepare and train data',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(2),
        tags=['full'],
) as dag:
    t = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    scraper_path = os.path.join(t, "scraper", "collect.py")
    t1 = BashOperator(
        task_id='run-scraper',
        bash_command=f'PYTHONPATH={t} python3 {scraper_path}',
    )

    parser_path = os.path.join(t, "scraper", "parse.py")
    t2 = BashOperator(
        task_id='run-parser',
        bash_command=f'PYTHONPATH={t} python3 {parser_path}',
    )

    prepare_path = os.path.join(t, "predictor", "prepare.py")
    t3 = BashOperator(
        task_id='run-prepare',
        bash_command=f'PYTHONPATH={t} python3 {prepare_path}',
    )

    train_path = os.path.join(t, "predictor", "train.py")
    t4 = BashOperator(
        task_id='run-train',
        bash_command=f'PYTHONPATH={t} python3 {train_path}',
    )

    t1 >> t2 >> t3 >> t4