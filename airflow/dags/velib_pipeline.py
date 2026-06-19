from datetime import datetime

from airflow import DAG

from airflow.operators.bash import BashOperator


with DAG(
    dag_id="velib_pipeline",

    start_date=datetime(
        2026,
        1,
        1
    ),

    schedule="*/5 * * * *",

    catchup=False

) as dag:

    ingestion = BashOperator(
        task_id="ingestion",

        bash_command="""
        cd /opt/project/ingestion &&
        python main.py
        """
    )


    postgres_load = BashOperator(
        task_id="postgres_load",

        bash_command="""
        cd /opt/project/postgres &&
        python loader.py
        """
    )


    populate_time = BashOperator(
        task_id="populate_time_dimension",

        bash_command="""
        cd /opt/project/postgres
        python load_time_dimension.py
        """
    )


    alerting = BashOperator(
        task_id="alerting",

        bash_command="""
        cd /opt/project/automation &&
        python alert_checker.py
        """
    )


    ingestion >> postgres_load >> populate_time >> alerting