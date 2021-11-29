from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='consolidado_vendas',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2021, 11, 30),
    template_searchpath='/usr/local/airflow/include',
    catchup=False
) as dag:


    Consolidado = BashOperator(
        task_id='Consolidado',
        bash_command='python3 /mnt/c/Users/virodrig/PycharmProjects/pythonProject/dags/python/Consolidado.py',
    )

    TweepyScript = BashOperator(
       task_id='TweepyScript',
        bash_command='python3 /mnt/c/Users/virodrig/PycharmProjects/pythonProject/dags/python/Tweepy.py',
    )

Consolidado >> TweepyScript
