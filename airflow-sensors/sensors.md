<h1>Airflow Sensors</h1>

<h2>Topics</h2>
<ul>
<li>What's a Sensor?</li>
<li>Make your Sensors better;</li>
<li>Use case: DAG Dependencies with the ExternalTaskSensor;</li>
<li>Smart Sensors?</li>
</ul>

<h2>What's a Sensor?</h2>
<p>Sensors are a special type of Operator that are designed to do exactly one thing - wait for something to occur. It can be time-based, or waiting for a file, or an external event, but all they do is wait until something happens, and then succeed so their downstream tasks can run. <sup>1</sup></p> 
<p>
Basically a Sensor checks if the Condition is True or False. Each sensor has its own condition to check. If it's true, otherwise it will wait until a deifned time (poke interval) and check it again.
<p>
<p>
The Sensor operators are derived from the class BaseSensorOperator and inherit these atributes<sup>2</sup>
<p>
<h3>BaseSensorOperator parameters</h3>
<ul>
<li>
<b>soft_fail (<code>bool</code>):</b>
Set to true to mark the task as SKIPPED<sup>3</sup> on failure
</li>
<li>
<b>poke_interval (<code>datetime.timedelta | float</code>):</b>
Time that the job should wait in between each try. Can be <code>timedelta</code> or <code>float</code> seconds.
</li>
<li>
<b>timeout (<code>datetime.timedelta | float</code>):</b>
Time elapsed before the task times out and fails. Can be <code>timedelta</code> or <code>float</code> seconds. This should not be confused with <code>execution_timeout</code> of the <code>BaseOperator</code> class. <code>timeout</code> measures the time elapsed between the first poke and the current time (taking into account any reschedule delay between each poke), while <code>execution_timeout</code> checks the running time of the task (leaving out any reschedule delay). In case that the <code>mode</code> is <code>poke</code> (see below), both of them are equivalent (as the sensor is never rescheduled), which is not the case in <code>reschedule</code> mode.
</li>
<li>
<b>mode (<code>str</code>):</b>
How the sensor operates. Options are: <code>{ poke | reschedule }</code>, default is <code>poke</code>. When set to <code>poke</code> the sensor is taking up a worker slot for its whole execution time and sleeps between pokes. Use this mode if the expected runtime of the sensor is short or if a short poke interval is required. Note that the sensor will hold onto a worker slot and a pool slot for the duration of the sensor’s runtime in this mode. When set to <code>reschedule</code> the sensor task frees the worker slot when the criteria is not yet met and it’s rescheduled at a later time. Use this mode if the time before the criteria is met is expected to be quite long. The poke interval should be more than one minute to prevent too much load on the scheduler.
</li>
<li>
<b>exponential_backoff (<code>bool</code>):</b>
Allow progressive longer waits between pokes by using exponential backoff algorithm
</li>
<li>
<b>max_wait (<code>datetime.timedelta | float | None</code>):</b>
Maximum wait interval between pokes, can be timedelta or float seconds
</li>
<li>
<b>silent_fail (<code>bool</code>):</b>
If true, and poke method raises an exception different from <code>AirflowSensorTimeout</code>, <code>AirflowTaskTimeout</code>, <code>AirflowSkipException</code> and <code>AirflowFailException</code>, the sensor will log the error and continue its execution. Otherwise, the sensor task fails, and it can be retried based on the provided retries parameter.
</li>
</ul>

<h3>Types of Sensors</h3>
<h4>FileSensor</h4>
<code>class airflow.sensors.filesystem.FileSensor(*, filepath, fs_conn_id='fs_default', **kwargs)</code>
<br><br>
<p>Use the FileSensor to detect files appearing your local filesystem. You need to have connection defined to use it (pass connection id via <code>fs_conn_id</code>). Default connection is <code>fs_default</code>.</p>
<ul>
<li>
<b>fs_conn_id (<code>str</code>):</b>
Reference to the File (path) connection id
</li>
<li>
<b>sql (<code>str</code>):</b>
File or folder name (relative to the base path set within the connection), can be a glob.
</li>
</ul>

<h4>ExternalTaskSensor</h4>
<code>class airflow.sensors.external_task.ExternalTaskSensor(*, external_dag_id: str, external_task_id: Optional[str] = None, allowed_states: Optional[Iterable[str]] = None, failed_states: Optional[Iterable[str]] = None, execution_delta: Optional[datetime.timedelta] = None, execution_date_fn: Optional[Callable] = None, check_existence: bool = False, **kwargs)</code>
<br><br>
<p>Waits for a different DAG or a task in a different DAG to complete for a specific <code>execution_date</code>.</p>
<ul>
<li>
<b>external_dag_id (<code>str</code>):</b>
The dag_id that contains the task you want to wait for
</li>
<li>
<b>external_task_id (<code>str | None</code>):</b>
The task_id that contains the task you want to wait for. If None (default value) the sensor waits for the DAG
</li>
</ul>

<h4>DateTime</h4>
<h4>HttpSensor</h4>
<h4>SqlSensor</h4>
<code>class airflow.sensors.sql.SqlSensor(*, conn_id, sql, parameters=None, success=None, failure=None, fail_on_empty=False, **kwargs)</code>
<br><br>
<p>Run a SQL statement repeatedly until a criteria match. </p>
<h5>Parameters</h5>
<ul>
<li>
<b>conn_id (<code>str</code>):</b>
The connection to run the sensor against
</li>
<li>
<b>sql (<code>str</code>):</b>
The sql to run. To pass, it needs to return at least one cell that contains a non-zero / empty string value.
</li>
<li>
<b>parameters (<code>dict | iterable</code>):</b>
The parameters to render the SQL query with (optional).
</li>
<li>
<b>success (<code>bool</code>):</b>
Success criteria for the sensor is a Callable that takes first_cell as the only argument, and returns a boolean (optional)
</li>
<li>
<b>failure (<code>bool</code>):</b>
Failure criteria for the sensor is a Callable that takes first_cell as the only argument and return a boolean (optional)
</li>
<li>
<b>fail_on_empty (<code>bool</code>):</b>
Failure criteria for the sensor is a Callable that takes first_cell as the only argument and return a boolean (optional)
</li>
</ul>
<h4>PythonSensor</h4>
<h4>SubDagOperator (it's a Sensor, despite the name)</h4>
<h4>Others.... check it at the Airflow Docs <sup>2</sup></h4>

<h3>SmartSensors</h3>


<h2>References</h2>
<sup>2</sup><a link="https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/base/index.html">BaseSensorOperator</a>