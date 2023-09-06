from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

@task()
def sum_task(x, y):
    return x + y

@dag(
    dag_id="dag_for_test_dynamic_task",
    description="""This DAG is being used for learning dynamic tasks
                """,
    start_date=datetime(2023, 8, 28, 7, 0, 0),
    schedule=timedelta(days=2),
    default_view="graph",
    template_searchpath="../../opt/airflow/"
)
def a_dag_for_dynamic_task():
    _sum_task = sum_task.partial(y=19).expand(x=[1, 2, 3])
    _bash_task_expand = BashOperator.partial(
        task_id = "bash_task_expand"
        ).expand(
            bash_command=[
                "echo $WORD",
                "echo $expr length $WORD",
                "echo ${WORD//e/X}"
            ],
            env=[
                {"WORD": "hello"},
                {"WORD": "tea"},
                {"WORD": "goodbye"}
            ]
        )
    _bash_task_expand_kwargs = BashOperator.partial(
        task_id = "bash_task_expand_kwargs"
        ).expand(
            [
                {"bash_command": "echo $WORD", "env": {"WORD": "hello"}},
                {"bash_command": "echo $expr length $WORD", "env": {"WORD": "tea"}},
                {"bash_command": "echo ${WORD//e/X}", "env": {"WORD": "goodbye"}}
            ]
        )
    _sum_task
    _bash_task_expand
    _bash_task_expand_kwargs

a_dag_for_dynamic_task()