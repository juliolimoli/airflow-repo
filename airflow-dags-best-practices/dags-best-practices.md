<h1>Airflow Dags Best Practices</h1>
<sup>*From Astronomer Webinar</sup>


<h2>Topics</h2>
<ul>
<li>Basics concepts</li>
<li>Best practices</li>
</ul>
<h2>Basics concepts</h2>
<h3>DAGs</h3>
<p><a href="../airflow-dags/dags.md">Click here.</a></p>
<h3>Idempotency</h3>
<p>The property whereby an operation can be applied multiple times without changing the result.</p>
<h3>Orchestration</h3>
<p>Airflow is designed to be an Orchestrator, not an execution framework.</p>
<h2>Best practices</h2>
<h3>Use it as an orchestrator, not executor.</h3>
<p>In practice, this means:</p>
<ul>
<li>DO use Airflow Providers to orchestrate jobs with other tools</li>
<li>DO offload heavy processing to execution frameworks (e.g. Spark)</li>
<li>DO use an ELT framework wherever possible</li>
<li>DO use intermediary data storage</li>
<li>DON'T pull large datasets into a task and process with Pandas</li>
</ul>

<h3>Use template Fields, Variables and Macros <sup>1</sup></h3>
<p>Making fields templatable, or using built-in Airflow variables and macros allows them to be set dynamically using environment variables with jinja templating.</p>
<p>This helps with:</p>
<ul>
<li>Idempotency</li>
<li>Situations where you have to re-run portions of your DAG</li>
<li>Maintainability</li>
</ul>

<h3>Keep clean DAG files</h3>
<p>Focus on readability and performance when creating your DAG files:</p>
<ul>
<li>Use a consistent project structure</li>
<li>Define one DAG per Python file</li>
<li>Avoid top level code in your DAG files</li>
</ul>
<p>In general, remember all DAG code is parsed every min_file_process_interval.</p>

<h3>Some helpful Airflow features</h3>
<p>Airflow 2.0+ has many new features that help improve the DAG authoring experience.</p>
<ul>
<li><b>TaskGroups: </b>Use task groups instead of subdags to visually organize your DAGs.</li>
<li><b>XComs Backends: </b>When passing data between tasks, use an XCom backend to avoid overloading your metastore.</li>
<li><b>TaskFlow API: </b>Use the TaskFlow API to cleanly define Python operators and pass data between them.</li>
<li><b>Deferrable Operators: </b>Use deferrable operators where available to free up processing power in your
Airflow workers.</li>
<li><b>Hide secrets in logs: </b>Set hide sensitive var conn fields to True in your airflow.cfg to ensure sensitive variables are masked in the logs and UI.</li>
<li><b>TimeTables: </b>Use custom timetables to implement schedules that cron alone doesn't support, rather than complex branching or multiple DAG copies.</li>
</ul>

<h3>Other Best Practices</h3>
<ul>
<li>Keep tasks atomic.</li>
<li>Use incremental record filtering.</li>
<li>Use a static start date.</li>
<li>Change the name of your DAG when you change the start date.</li>
<li>Choose a consistent method when setting task dependencies.</li>
</ul>

<sup>1</sup><a href="">Airflow built-in Variables</a>