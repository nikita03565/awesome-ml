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
        'prepare-data',
        default_args=default_args,
        description='Lemmatizing and stemming test from csv',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(2),
        tags=['prepare'],
) as dag:
    t = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    parser_path = os.path.join(t, "predictor", "prepare.py")
    t1 = BashOperator(
        task_id='run-prepare',
        bash_command=f'PYTHONPATH={t} python {parser_path}',
    )
