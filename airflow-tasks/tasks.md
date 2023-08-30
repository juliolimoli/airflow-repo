<h1>Airflow Tasks</h1>

<h2>Topics</h2>
<ul>
<li>What's a Task?</li>
<li>Types of Tasks</li>
<li>Tasks Relationships/Dependencies</li>
<li>Task Instances</li>
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

<h2>Tasks Relationships/Dependencies</h2>
<p>The key part of using Tasks is defining how they relate to each other - their dependencies, or as we say in Airflow, their upstream and downstream tasks. You declare your Tasks first, and then you declare their dependencies second.</p>
<p><a href="../airflow-dags/dags.md#task-dependencies-inside-a-dag">See here</a> how to setup the dependencies.</p>

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