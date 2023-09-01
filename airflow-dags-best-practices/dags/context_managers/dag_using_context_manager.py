import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator

@task(task_id="second_task")
def second_task_test(**kwargs):
    print("Printing kwargs:", kwargs)
    print(kwargs['ds'])
    return "End second task"

with DAG(
    dag_id="context_manager_test_dag",
    description="""A DAG using the context manager with basic parameters and task. 
                    The main goal is get used to dags parameters.""",
    start_date=datetime.datetime(2023, 8, 28), 
    schedule="@daily",
    owner_links = {"Júlio Limoli Silva": "mailto:jls@airflow.com"},
    tags = ["learning", "parameters"]
    ):
    EmptyOperator(task_id="empty_operator_first_task") >> second_task_test()