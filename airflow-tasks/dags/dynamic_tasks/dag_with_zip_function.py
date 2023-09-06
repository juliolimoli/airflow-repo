from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator

@task()
def get_123():
    return [1, 2, 3]

@task()
def get_abc():
    return ["a", "b", "c"]

@task()
def multiply(input):
    number = input[0]
    letter = input[1]
    return number * letter

@dag(
    dag_id="dag_for_test_dynamic_task_with_zip_function",
    description="""This DAG is being used for learning dynamic tasks
                """,
    start_date=datetime(2023, 8, 28, 7, 0, 0),
    schedule=timedelta(days=2),
    default_view="graph",
    template_searchpath="../../opt/airflow/",
    catchup=False
)
def a_dag_for_dynamic_task_zip():
    _multiply = multiply.partial().expand(
        input = get_123().zip(get_abc())
    )
    _multiply
    

a_dag_for_dynamic_task_zip()