import datetime

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator

@task(task_id="task_return_string")
def task_test_general_value(ti=None):
    ti.xcom_push(key="xcom_test_key", value="some_test_value")

@task(task_id="task_return_string_2")
def task_test_general_value_2(ti=None):
    ti.xcom_push(key="xcom_test_key", value="some_test_value")

@task(task_id="task_takes_the_return_string")
def task_test_get_returned(ti=None):
    xcom_value = ti.xcom_pull(task_ids=["task_return_string", "task_return_string_2"], key="xcom_test_key")
    print(xcom_value)

@dag(
    dag_id="test1_dag_empty",
    description="""The first test DAG wiht basic parameters and task. 
                    The main goal is get used to dags parameters.""",
    start_date=datetime.datetime(2023, 8, 28), 
    schedule="@daily",
    owner_links = {"Júlio Limoli Silva": "mailto:jls@airflow.com"},
    tags = ["learning", "parameters"],
    default_view="graph"
    )
def a_simple_and_first_test_dag():
    (task_test_general_value() 
     >> task_test_general_value_2()
     >> task_test_get_returned()
    )

a_simple_and_first_test_dag()