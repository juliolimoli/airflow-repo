<h1>Airflow Tasks</h1>

<div style="text-align: center; font-size: 8px;">
    <span>If you want to see about Dynamic Tasks: </span><span><b><a href="./dynamic_tasks.md">Click Here</a></b></span>
</div>

<h2>Topics</h2>
<ul>
<li>What's a Task?</li>
<li>Types of Tasks</li>
<ul>
<li>Operators</li>
<li>Sensors</li>
<li>TaskFlow-decorated <code>@task</code></li>
</ul>
<li>Tasks Relationships/Dependencies</li>
<li>Task Instances</li>
<li>Timeouts</li>
<li>Special Exceptions</li>
<li>Zombie/Undead Tasks</li>
<li>Deferrable Operators</li>
</ul>

<h2>What's a Task?</h2>
<p>A Task is the basic unit of execution in Airflow. Tasks are arranged into <a href="../airflow-dags/dags.md">DAGs</a>, and then have upstream and downstream dependencies set between them into order to express the order they should run in.</p>

<h2>Types of Tasks</h2>
<p>There are three basic kinds of Task:</p>
<ul>
<li><b>Operators:</b> predefined task templates that you can string together quickly to build most parts of your DAGs.</li>
<li><b>Sensors:</b> a special subclass of Operators which are entirely about waiting for an external event to happen.</li>
<li><b>TaskFlow-decorated <code>@task</code>:</b> a custom Python function packaged up as a Task.</li>
</ul>
<p>Internally, these are all actually subclasses of Airflow’s <code>BaseOperator</code>, and the concepts of Task and Operator are somewhat interchangeable, but it’s useful to think of them as separate concepts - essentially, Operators and Sensors are templates, and when you call one in a DAG file, you’re making a Task.</p>
<h3>Operators</h3>
<h4>PythonOperator<sup>1</sup></h4>
<p>Use the <code>@task</code> decorator to execute Python callables.</p>
<h4>BashOperator</h4>
<p>Use the BashOperator to execute commands in a Bash shell.</p>
<h4>EmailOperator</h4>
<p></p>
<h4>BranchDateTimeOperator</h4>
<h4>BranchPythonOperator</h4>
<p>A workflow can “branch” or follow a path after the execution of this task.</p>

<h4>ExternalPythonOperator</h4>
<p>The Airflow provides some built in libraries and tools that can help when the common PythonOperator is used. Sometimes, it's necessary to use some different tools or libraries that is not built in, some it might be necessary develop your own operator, that can point to a virtual environment built by yourself, totally customized.</p>
<p>The operator takes Python binary as python parameter. Note, that even in case of virtual environment, the python path should point to the python binary inside the virtual environment (usually in bin subdirectory of the virtual environment). Contrary to regular use of virtual environment, there is no need for activation of the environment. Merely using python binary automatically activates it. In both examples below PATH_TO_PYTHON_BINARY is such a path, pointing to the executable Python binary.</p>
<p style="background-color: #000; color: yellow;">Unfortunately Airflow does not support serializing var and ti / task_instance due to incompatibilities with the underlying library. For Airflow context variables make sure that Airflow is also installed as part of the virtualenv environment in the same version as the Airflow version the task is run on. Otherwise you won’t have access to the most context variables of Airflow in op_kwargs.</p>

<h2>Tasks Relationships/Dependencies</h2>
<p>The key part of using Tasks is defining how they relate to each other - their dependencies, or as we say in Airflow, their upstream and downstream tasks. You declare your Tasks first, and then you declare their dependencies second.</p>
<p><a href="../airflow-dags/dags.md#task-dependencies-inside-a-dag">See here</a> how to setup the dependencies.</p>
<p>Tasks don’t pass information to each other by default, and run entirely independently. If you want to pass information from one Task to another, you should use <a>XComs</a>.</p>

<h2>Tasks Instances</h2>
<p>Much in the same way that a DAG is instantiated into a DAG Run each time it runs, the tasks under a DAG are instantiated into Task Instances.</p>
<p>An instance of a Task is a specific run of that task for a given DAG (and thus for a given data interval). They are also the representation of a Task that has state, representing what stage of the lifecycle it is in.</p>

<p>The possible states for a Task Instance are:</p>
<ul>
<li><b>none</b>: The Task has not yet been queued for execution (its dependencies are not yet met)</li>
<li><b>scheduled</b>: The scheduler has determined the Task’s dependencies are met and it should run</li>
<li><b>queued</b>: The task has been assigned to an Executor and is awaiting a worker</li>
<li><b>running</b>: The task is running on a worker (or on a local/synchronous executor)</li>
<li><b>success</b>: The task finished running without errors</li>
<li><b>shutdown</b>: The task was externally requested to shut down when it was running</li>
<li><b>restarting</b>: The task was externally requested to restart when it was running</li>
<li><b>failed</b>: The task had an error during execution and failed to run</li>
<li><b>skipped</b>: The task was skipped due to branching, LatestOnly, or similar.</li>
<li><b>upstream_failed</b>: An upstream task failed and the Trigger Rule says we needed it</li>
<li><b>up_for_retry</b>: The task failed, but has retry attempts left and will be rescheduled.</li>
<li><b>up_for_reschedule</b>: The task is a Sensor that is in reschedule mode</li>
<li><b>deferred</b>: The task has been deferred to a trigger</li>
<li><b>removed</b>: The task has vanished from the DAG since the run started</li>
</ul>
<img src="https://airflow.apache.org/docs/apache-airflow/stable/_images/task_lifecycle_diagram.png" style="background-color: white;">
<p>Ideally, a task should flow from <code>none</code>, to <code>scheduled</code>, to <code>queued</code>, to <code>running</code>, and finally to <code>success</code>.</p>

<h2>Timeouts</h2>
<p>The task timeout in Airflow refers to the maximum amount of time a task is allowed to run before it is forcibly marked as failed and terminated by the Airflow scheduler. This is useful for preventing tasks from running indefinitely, especially if they encounter issues that prevent them from completing within a reasonable time frame. Task timeouts are set using the execution_timeout parameter when defining a task.</p>

<h2>SLAs</h2>
<p>An SLA, or a Service Level Agreement, is an expectation for the maximum time a Task should be completed relative to the Dag Run start time. If a task takes longer than this to run, it is then visible in the “SLA Misses” part of the user interface, as well as going out in an email of all tasks that missed their SLA.</p>
<p>Tasks over their SLA are not cancelled, though - they are allowed to run to completion. If you want to cancel a task after a certain runtime is reached, you want Timeouts instead.</p>
<p>To set an SLA for a task, pass a <code>datetime.timedelta</code> object to the Task/Operator’s sla parameter. You can also supply an <code>sla_miss_callback</code> that will be called when the SLA is missed if you want to run your own logic.</p>

<h3><code>sla_miss_callback</code></h3>
<p>You can also supply an <code>sla_miss_callback</code> that will be called when the SLA is missed if you want to run your own logic. The function signature of an <code>sla_miss_callback</code> requires 5 parameters.<p>
<ol>
<li><b>dag: </b>Parent DAG Object for the DAGRun in which tasks missed their SLA.</li>
<li><b>task_list: </b>String list (new-line separated, \n) of all tasks that missed their SLA since the last time that the sla_miss_callback ran.</li>
<li><b>blocking_task_list: </b>Any task in the DAGRun(s) (with the same execution_date as a task that missed SLA) that is not in a SUCCESS state at the time that the sla_miss_callback runs. i.e. ‘running’, ‘failed’. These tasks are described as tasks that are blocking itself or another task from completing before its SLA window is complete.</li>
<li><b>slas: </b>List of SlaMiss objects associated with the tasks in the task_list parameter.</li>
<li><b>blocking_tis: </b>List of the TaskInstance objects that are associated with the tasks in the blocking_task_list parameter.</li>
</ol>
<code>

    def my_sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    ...
</code>
<code>

    def sla_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(
        "The callback arguments are: ",
        {
            "dag": dag,
            "task_list": task_list,
            "blocking_task_list": blocking_task_list,
            "slas": slas,
            "blocking_tis": blocking_tis,
        },
    )

    @dag(
        schedule="*/2 * * * *",
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        sla_miss_callback=sla_callback,
        default_args={"email": "email@example.com"},
    )
    def example_sla_dag():
        @task(sla=datetime.timedelta(seconds=10))
        def sleep_20():
            """Sleep for 20 seconds"""
            time.sleep(20)

        @task
        def sleep_30():
            """Sleep for 30 seconds"""
            time.sleep(30)

        sleep_20() >> sleep_30()


    example_dag = example_sla_dag()

</code>

<h2>Special Exceptions</h2>

<p>If you want to control your task’s state from within custom Task/Operator code, Airflow provides two special exceptions you can raise:</p>
<ul>
<li><code>AirflowSkipException</code> will mark the current task as skipped</li>
<li><code>AirflowFailException</code> will mark the current task as failed ignoring any remaining retry attempts</li>
</ul>
<p>
These can be useful if your code has extra knowledge about its environment and wants to fail/skip faster - e.g., skipping when it knows there’s no data available, or fast-failing when it detects its API key is invalid (as that will not be fixed by a retry).</p>

<h2>Zombie/Undead Tasks</h2>
<p>No system runs perfectly, and task instances are expected to die once in a while. Airflow detects two kinds of task/process mismatch:</p>
<ul>
<li>Zombie tasks are tasks that are supposed to be running but suddenly died (e.g. their process was killed, or the machine died). Airflow will find these periodically, clean them up, and either fail or retry the task depending on its settings.</li>
<li>Undead tasks are tasks that are not supposed to be running but are, often caused when you manually edit Task Instances via the UI. Airflow will find them periodically and terminate them.</li>
</ul>

<h2>Deferrable Operators</h2>
<p>First, let's understand what happens in a task process: the scheduler submits a task to the executor -> then a worker executes the tasks until it completes.</p>
<p>This makes sense and works well if your task is actually doing something, such as: sending a request, a query, processing data, etc.</p> 
<p>But if the task is waiting for something, like a response, it will leave it working without any need. It gives an opportunity cost.</p>

<sup>1</sup><span><a href="https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html">PythonOperator</a></span>