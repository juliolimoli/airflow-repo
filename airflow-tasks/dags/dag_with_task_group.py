from datetime import datetime, timedelta
from random import randint

from airflow.decorators import dag, task, task_group
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator

@task(task_id="number_generator")
def number_generator_task(ti=None):
    ti.xcom_push(key="number", value=randint(1,20))

_number_generator_task = number_generator_task()

@task(task_id="even_task_printer")
def even_task_printer(ti=None):
    number = ti.xcom_pull(
        task_ids="number_generator", 
        key="number"
        )
    print(number)

@task(task_id="even_task_duplicator")
def even_task_duplicator(ti=None):
    number = ti.xcom_pull(
        task_ids="number_generator", 
        key="number"
        )
    duplicated_number = number*2
    ti.xcom_push(
        key="duplicated_number",
        value=duplicated_number
        )
    print(duplicated_number)

@task(task_id="odd_task_printer")
def odd_task_printer(ti=None):
    number = ti.xcom_pull(
        task_ids="number_generator", 
        key="number"
        )
    print(number)

@task(task_id="odd_task_duplicator")
def odd_task_duplicator(ti=None):
    number = ti.xcom_pull(
        task_ids="number_generator", 
        key="number"
        )
    duplicated_number = number*2
    ti.xcom_push(
        key="duplicated_number",
        value=duplicated_number
        )
    print(duplicated_number)


@task(task_id="final_task", trigger_rule="none_failed")
def final_task(ti=None):
    number = ti.xcom_pull(
        task_ids="number_generator", 
        key="number"
        )
    duplicated_number = ti.xcom_pull(
        task_ids=[
            "even_taskgroup.even_task_duplicator",
            "odd_taskgroup.odd_task_duplicator"], 
        key="duplicated_number"
        )
    print(f"""The generated number was: {number}.
            The duplicated is: {duplicated_number}
    """)
_final_task = final_task()

@dag(
    dag_id="dag_with_task_groups",
    description="""This DAG is being used for learning how to
                    group tasks.
                """,
    start_date=datetime(2023, 8, 28, 7, 0, 0),
    schedule=timedelta(days=2),
    catchup=False,
    default_view="graph",
    template_searchpath="../../opt/airflow/"
)
def dag_with_task_groups():

    @task.branch(task_id="branching_operator")
    def odd_or_even_branching(ti=None):
        number = ti.xcom_pull(
                task_ids="number_generator", 
                key="number"
                )
        print(number)
        if number % 2 == 0:
            return 'even_taskgroup.even_task_printer'
        else:
            return 'odd_taskgroup.odd_task_printer'

    _odd_or_even_branching = odd_or_even_branching()

    @task_group(group_id="even_taskgroup")
    def even_taskgroup(ti=None):
        _even_task_printer = even_task_printer()
        _even_task_duplicator = even_task_duplicator()

        _even_task_printer >> _even_task_duplicator
    
    @task_group(group_id="odd_taskgroup")
    def odd_taskgroup(ti=None):
        _odd_task_printer = odd_task_printer()
        _odd_task_duplicator = odd_task_duplicator()

        _odd_task_printer >> _odd_task_duplicator

    _even_taskgroup = even_taskgroup()
    _odd_taskgroup = odd_taskgroup()

    (_number_generator_task
     >> _odd_or_even_branching
     >> [_even_taskgroup, _odd_taskgroup]
     >> _final_task
    )

dag_with_task_groups()