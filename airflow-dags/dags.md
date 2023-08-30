<h1>Airflow Dags</h1>

<h2>Topics</h2>
<ul>
<li>What's a DAG?</li>
<li>How to create DAGs?</li>
<li>DAGs parameters</li>
<li>Tasks dependencies inside a DAG</li>
</ul>
<h2>What's a DAG?</h2>
<p>A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.</p> 
<img src="https://media.licdn.com/dms/image/C5612AQFCYaFYTx75qA/article-inline_image-shrink_400_744/0/1567658233668?e=1697673600&v=beta&t=yBPHBk5SodHQ0zQN1G6pf5TB0iKHxQXpCCLEw6RWkYE" alt="DAG example picture">

<h2>How to create DAGs</h2>
<p>There are three ways to declare a DAG - either you can use a context manager, which will add the DAG to anything inside it implicitly:</p>
<h3>Context Manager</h3>
<code>

    import datetime

    from airflow import DAG
    from airflow.operators.empty import EmptyOperator


    with DAG(
        dag_id="my_dag_name",
        start_date=datetime.datetime(2021, 1, 1),
        schedule="@daily",
        ):

        EmptyOperator(task_id="task")
</code>
<h3>Standard Constructor</h3>
<p>Passing the DAG into any operators you use</p>
<code>

    import datetime

    from airflow import DAG
    from airflow.operators.empty import EmptyOperator

    my_dag = DAG(
        dag_id="my_dag_name",
        start_date=datetime.datetime(2021, 1, 1),
        schedule="@daily",
    )
    EmptyOperator(task_id="task", dag=my_dag)
</code>
<h3>DAG Decorator</h3>
<p>It turns your function a DAG generator.</p>
<code>

    import datetime

    from airflow.decorators import dag
    from airflow.operators.empty import EmptyOperator


    @dag(start_date=datetime.datetime(2021, 1, 1), schedule="@daily")
    def generate_dag():
        EmptyOperator(task_id="task")


    generate_dag()
</code>

<p style="font-weight: bold; color: yellow; background-color: black;">DAGs are nothing without Tasks to run, and those will usually come in the form of either Operators, Sensors or TaskFlow.</p>

<h2>DAGs parameters</h2>
<ul>
<li>
<b>dag_id (<code>str</code>):</b>
The id of the DAG; must consist exclusively of alphanumeric characters, dashes, dots and underscores.
</li>
<li>
<b>description (<code>str | None</code>):</b>
The description for the DAG to e.g. be shown on the webserver.
</li>
<li>
<b>schedule (<code>ScheduleArg</code>):</b>
Defines the rules according to which DAG runs are scheduled. Can accept cron string, timedelta object, Timetable, or list of Dataset objects. See also Customizing DAG Scheduling with Timetables.<sup>1</sup>
</li>
<li>
<b>start_date (<code>datetime.datetime | None</code>):</b>
The timestamp from which the scheduler will attempt to backfil
</li>
<li>
<b>end_date (<code>datetime.datetime | None</code>):</b>
A date beyond which your DAG won’t run, leave to None for open-ended scheduling.
</li>
<li>
<b>template_searchpath (<code>str | Iterable[str] | None</code>):</b>
This list of folders (non-relative) defines where jinja will look for your templates. Order matters. Note that jinja/airflow includes the path of your DAG file by default.
</li>
<li>
<b>template_undefined (<code>type[jinja2.StrictUndefined]</code>):</b>
Template undefined type.
</li>
<li>
<b>user_defined_macros (<code>dict | None</code>):</b>
A dictionary of macros that will be exposed in your jinja templates. For example, passing <code>dict(foo='bar')</code> to this argument allows you to <code>{{ foo }}</code>in all jinja templates related to this DAG. Note that you can pass any type of object here.
</li>
<li>
<b>user_defined_filters (<code>dict | None</code>):</b>
A dictionary of filters that will be exposed in your jinja templates. For example, passing <code>dict(hello=lambda name: 'Hello %s' % name)</code> to this argument allows you to <code>{{ 'world' | hello }}</code> in all jinja templates related to this DAG.
</li>
<li>
<b>default_args (<code>dict | None</code>):</b>
A dictionary of default parameters to be used as constructor keyword parameters when initialising operators. Note that operators have the same hook, and precede those defined here, meaning that if your dict contains ‘depends_on_past’: True here and ‘depends_on_past’: False in the operator’s call default_args, the actual value will be False.
</li>
<li>
<b>params (<code>collections.abc.MutableMapping | None</code>):</b>
A dictionary of DAG level parameters that are made accessible in templates, namespaced under params. These params can be overridden at the task level.
</li>
<li>
<b>max_active_tasks (<code>int</code>):</b>
The number of task instances allowed to run concurrently
</li>
<li>
<b>max_active_runs (<code>int</code>):</b>
Maximum number of active DAG runs, beyond this number of DAG runs in a running state, the scheduler won’t create new active DAG runs

<b>dagrun_timeout (<code>datetime.timedelta | None</code>):</b>
specify how long a DagRun should be up before timing out / failing, so that new DagRuns can be created
</li>
<li>
<b>sla_miss_callback (<code>cNone | SLAMissCallback | list[SLAMissCallback]</code>):</b>
specify a function or list of functions to call when reporting SLA timeouts. See sla_miss_callback for more information about the function signature and parameters that are passed to the callback.
</li>
<li>
<b>default_view (<code>str</code>):</b>
Specify DAG default view (grid, graph, duration, gantt, landing_times), default grid
</li>
<li>
<b>orientation (<code>str</code>):</b>
Specify DAG orientation in graph view (LR, TB, RL, BT), default LR
</li>
<li>
<b>catchup (<code>bool</code>):</b>
Perform scheduler catchup (or only run latest)? Defaults to True
</li>
<li>
<b>on_failure_callback (<code>None | DagStateChangeCallback | list[DagStateChangeCallback]</code>):</b>
A function or list of functions to be called when a DagRun of this dag fails. A context dictionary is passed as a single parameter to this function.
</li>
<li>
<b>on_success_callback (<code>None | DagStateChangeCallback | list[DagStateChangeCallback]</code>):</b>
same above
</li>
<li>
<b>access_control (<code>dict | None</code>):</b>
Specify optional DAG-level actions, e.g., “{‘role1’: {‘can_read’}, ‘role2’: {‘can_read’, ‘can_edit’, ‘can_delete’}}”
</li>
<li>
<b>is_paused_upon_creation (<code>bool | None</code>):</b>
Specifies if the dag is paused when created for the first time. If the dag exists already, this flag will be ignored. If this optional parameter is not specified, the global config setting will be used.
</li>
<li>
<b>jinja_environment_kwargs (<code>dict | None</code>):</b>
additional configuration options to be passed to Jinja Environment for template rendering
</li>
<li>
<b>render_template_as_native_obj (<code>bool</code>):</b>
If True, uses a Jinja NativeEnvironment to render templates as native Python types. If False, a Jinja Environment is used to render templates as string values.
</li>
<li>
<b>tags (<code>list[str] | None</code>):</b>
List of tags to help filtering DAGs in the UI.
</li>
<li>
<b>owner_links (<code>dict[str, str] | None</code>):</b>
Dict of owners and their links, that will be clickable on the DAGs view UI. Can be used as an HTTP link (for example the link to your Slack channel), or a mailto link. e.g: {“dag_owner”: “https://airflow.apache.org/”}
</li>
<li>
<b>auto_register (<code>bool</code>):</b>
Automatically register this DAG when it is used in a <code>with</code> block
</li>
<li>
<b>fail_stop (<code>bool</code>):</b>
Fails currently running tasks when task in DAG fails. Warning: A fail stop dag can only have tasks with the default trigger rule (“all_success”). An exception will be thrown if any task in a fail stop dag has a non default trigger rule.
</li>
</ul>

<h2>Tasks dependencies inside a DAG</h2>
<p>A Task/Operator does not usually live alone; it has dependencies on other tasks (those upstream of it), and other tasks depend on it (those downstream of it). Declaring these dependencies between tasks is what makes up the DAG structure (the edges of the directed acyclic graph).</p>
<p>There are two main ways to declare individual task dependencies:</p>
<ol>
<li>Bitshift operators (RECOMMENDED ONE): <code>>></code> and <code><<</code></li>
<code>

    first_task >> [second_task, third_task]
    third_task << fourth_task
</code>
<li>Explicits methods: <code>set_upstream</code> and <code>set_downstream</code></li>
<code>

    first_task.set_downstream(second_task, third_task)
    third_task.set_upstream(fourth_task)
</code>
<li>Other more complex methods: <code>cross_downstream</code> and <code>chain</code></li>
<ol>
<li>cross_downstream</li>
<p>If you want to make two lists of tasks depend on all parts of each other, you can’t use either of the approaches above, so you need to use <code>cross_downstream</code>:</p>
<code>

    from airflow.models.baseoperator import cross_downstream

    # Replaces
    # [op1, op2] >> op3
    # [op1, op2] >> op4
    cross_downstream([op1, op2], [op3, op4])
</code>
<li>chain</li>
<p>And if you want to chain together dependencies, you can use <code>chain</code>:</p>
<code>

    from airflow.models.baseoperator import chain

    # Replaces op1 >> op2 >> op3 >> op4
    chain(op1, op2, op3, op4)

    # You can also do it dynamically
    chain(*[EmptyOperator(task_id='op' + i) for i in range(1, 6)])
</code>
</ol>
</ol>

<sup>1</sup><a href="https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html">TimeTables</a>