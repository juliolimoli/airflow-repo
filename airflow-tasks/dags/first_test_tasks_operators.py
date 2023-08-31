from datetime import datetime, timedelta

from airflow.decorators import dag
from airflow.operators.bash import BashOperator

bash_hello_airflow = 'echo "Hello Airflow!" && chmod +x ../../opt/airflow/scripts/bash/hello_from_file.sh '

@dag(
    dag_id="dag_for_operators_testing",
    description="""This DAG is being used for learning tasks
                    and its operators, such as Bash, Python, etc.
                    This DAG runs every other day.
                """,
    start_date=datetime(2023, 8, 28, 7, 0, 0),
    schedule=timedelta(days=2)
)
def a_test_dag_for_test_the_operators():
    (BashOperator(
        task_id="first_bash_task",
        bash_command=bash_hello_airflow
        ) 
    >> BashOperator(
        task_id="second_bash_task",
        bash_command="../../opt/airflow/scripts/bash/hello_from_file.sh "
        )
    )

a_test_dag_for_test_the_operators()