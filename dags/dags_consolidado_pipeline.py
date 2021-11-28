from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.papermill.operators.papermill import PapermillOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='consolidado_pipeline',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    template_searchpath='/usr/local/airflow/include',
    catchup=False
) as dag:


    consolidado = BashOperator(
        task_id='consolidado',
        bash_command='python3  /usr/local/lib/python3.8/dist-packages/airflow/example_dags/python/consolidado.py',
    )

#    TwitterSearch = BashOperator(
#       task_id='TwitterSearch',
#        bash_command='python /usr/local/lib/python3.8/dist-packages/airflow/example_dags/python/TwitterSearch.py',
#    )

    notebook_TwitterSearch = PapermillOperator(
            task_id="notebook_TwitterSearch",
            input_nb="/usr/local/lib/python3.8/dist-packages/airflow/example_dags/notebook_jupyter/TwitterSearch.ipynb",
            output_nb="/usr/local/lib/python3.8/dist-packages/airflow/example_dags/notebook_jupyter/out-{{ execution_date }}.ipynb",
            parameters={"execution_date": "{{ execution_date }}"},
        )

consolidado >> notebook_TwitterSearch