import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator

my_dag = DAG(
    dag_id="standard_constructor_test_dag",
    description="""A DAG using the standard constructor with basic parameters and task. 
                    The main goal is get used to dags parameters.""",
    start_date=datetime.datetime(2023, 8, 28), 
    schedule="@daily",
    owner_links = {"Júlio Limoli Silva": "mailto:jls@airflow.com"},
    tags = ["learning", "parameters"]
    )

@task(task_id="second_stage_first_task", dag=my_dag)
def second_stage_first_task(**kwargs):
    print("Printing kwargs:", kwargs)
    print(kwargs['ds'])
    return "End second stage first task task"

@task(task_id="second_stage_second_task", dag=my_dag)
def second_stage_second_task(**kwargs):
    print("Printing kwargs:", kwargs)
    print(kwargs['ds'])
    return "End second stage second task"

(EmptyOperator(task_id="empty_operator_first_task", dag=my_dag) 
 >> [second_stage_first_task(), second_stage_second_task()]
)