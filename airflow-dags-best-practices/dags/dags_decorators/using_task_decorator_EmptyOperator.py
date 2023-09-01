import datetime

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator

@task(task_id="second_task")
def second_task_test(**kwargs):
    print("Printing kwargs:", kwargs)
    print(kwargs['ds'])
    return "End second task"

@dag(
    dag_id="test1_dag_empty",
    description="""The first test DAG wiht basic parameters and task. 
                    The main goal is get used to dags parameters.""",
    start_date=datetime.datetime(2023, 8, 28), 
    schedule="@daily",
    owner_links = {"Júlio Limoli Silva": "mailto:jls@airflow.com"},
    tags = ["learning", "parameters"]
    )
def a_simple_and_first_test_dag():
    EmptyOperator(task_id="empty_operator_first_task") >> second_task_test()

a_simple_and_first_test_dag()