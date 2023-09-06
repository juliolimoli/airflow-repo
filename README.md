<h1>Airflow Study Repo</h1>
<span style="font-size: 8px;">** IMPORTANT: Almost everything here came from the Official Airflow Documentation or from the Astronomer Academy. **</span>

<h2>Airflow setup</h2>
<h3>With Docker</h3>
<ol>
<li>Install Docker;</li>
<li>Fetch Docker-compose file: <code>curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'</code></li>
<li>.env file: <code>echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env</code></li>
<li>docker-compose init: <code>docker-compose up airflow-init</code></li>
<li>docker-compose up: <code>docker-compose up</code></li>
</ol>
<h2>Airflow Main Topics</h2>
<p>All of these topics are distributed in each corresponding directory with its own documentation.</p>
<ul type="square">
<li><a href="./airflow-dags/dags.md">DAGs</a></li>
<li>Tasks</li>
<li>Sensors</li>
</ul>
<h2>Airflow Core Concepts</h2>
<h3>Webserver</h3>
<h4>Running commands in the airflow webserver</h4>
<code>
    
    docker exec <container-id> airflow ...
</code>
<h3>Scheduler</h3>
<h3><a href="https://docs.astronomer.io/learn/airflow-database">Metastore</a></h3>
<p>The metadata database is a core component of Airflow. It stores crucial information such as the configuration of your Airflow environment's roles and permissions, as well as all metadata for past and present DAG and task runs.</p>
<h3>Triggerer</h3>
<h3><a href="https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html#executor">Executor</a></h3>
<p>Executors are the mechanism by which task instances get run. They have a common API and are “pluggable”, meaning you can swap executors based on your installation needs.</p>
<p>Airflow can only have one executor configured at a time; this is set by the executor option in the [core] section of the configuration file.</p>
<h3>Queue</h3>
<h3>Worker</h3>
<h3>DAG</h3>

<h2>Airflow Architecture</h2>
<p>It's an open-source Linux and Python based workflow engine. It also has a Webserver and Web App UI.</p>

<img src="https://airflow.apache.org/docs/apache-airflow/stable/_images/arch-diag-basic.png">


<h2>Airflow Connections</h2>
<p>As a best practice, Airflow should be used as an orchestrator, so it might be common to access external services to actually do the transformation job. These external access requires connection to this services, such as API keys, username and password, secrets, etc.</p>
<p>To avoid hard these access informations, Airflow provides the feature of store some connections that're used in the tasks. They can be created in 3 different ways: </p>
<ul>
<li>The Airflow metadata database (Through UI or CLI);</li>
<li>An external Secret Backend;</li>
<li>In environment variables;</li>
</ul>
<p>The last one is important, because:</p>
<p>When you create a Connection in the database, each time a task needs this Connection, it requests the database. If you have many tasks, that can drastically increase the workload on your database.</p>
<p>With Connections in Environment Variables, the task doesn't need to request the database. Airflow checks if the corresponding Connection exists and grabs it without accessing the database. Again, at scale, this can help reduce the number of requests on your database.</p>
<p>On top of that, Connections defined in Environment Variables do not show up in the Airflow UI or using airflow connection list.</p>
<p>To define a Connection as an environment variable, you need to use the following naming convention:
AIRFLOW__CONN_{CONN_ID}='Your connection'.

Here {CONN_ID} corresponds to the connection id you want to give to your connection such as snowflake_default, postgres_default, etc. </p>

<h2>Trigger Rules</h2>
<p>All operators have a trigger_rule argument which defines the rule by which the generated task get triggered. The default value for trigger_rule is all_success and can be defined as “trigger this task when all directly upstream tasks have succeeded”. All other rules described here are based on direct parent tasks and are values that can be passed to any operator while creating tasks: <a href="https://airflow.apache.org/docs/apache-airflow/1.10.10/concepts.html#trigger-rules">See the documentation here</a></p>