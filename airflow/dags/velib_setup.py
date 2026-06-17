from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="velib_setup",

    start_date=datetime(
        2026,
        1,
        1
    ),

    schedule=None,

    catchup=False

) as dag:


    init_database = BashOperator(
        task_id="init_database",

        bash_command="""
        bash /opt/project/scripts/init_database.sh
        """
    )