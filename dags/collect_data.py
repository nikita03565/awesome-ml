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
        'collect-data',
        default_args=default_args,
        description='Collects html pages from pikabu',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(2),
        tags=['collect'],
) as dag:
    t = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    scraper_path = os.path.join(t, "scraper", "main.py")
    t1 = BashOperator(
        task_id='run-scraper',
        bash_command=f'PYTHONPATH={t} python {scraper_path}',
    )
