from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator

bash_hello_airflow = 'echo "Hello Airflow!" && chmod +x scripts/bash/hello_from_file.sh '

@task(task_id="task_1_python_get_xcom")
def task_1_python_get_xcom(ti=None):
    values_xcom = ti.xcom_pull(task_ids=["second_bash_task"])
    print("Values printed: ", values_xcom)

@dag(
    dag_id="dag_for_operators_testing",
    description="""This DAG is being used for learning tasks
                    and its operators, such as Bash, Python, etc.
                    This DAG runs every other day.
                """,
    start_date=datetime(2023, 8, 28, 7, 0, 0),
    schedule=timedelta(days=2),
    default_view="graph",
    template_searchpath="../../opt/airflow/"
)
def a_test_dag_for_test_the_operators():
    (BashOperator(
        task_id="first_bash_task",
        bash_command=bash_hello_airflow
        ) 
    >> BashOperator(
        task_id="second_bash_task",
        bash_command="scripts/bash/hello_from_file.sh ",
        do_xcom_push=True
        )
    >> task_1_python_get_xcom()
    #>> EmailOperator(
    #    task_id="task_email_operator",
    #    to="juliolimolisilva@gmail.com",
    #    subject="airflow EmailOperator testing",
    #    html_content="<h1>This is a test</h1>",
    #    trigger_rule='none_failed'
    #)
    )

a_test_dag_for_test_the_operators()