<h1>Airflow CLI</h1>

<h2>Airflow Infos</h2>
<p>Tells all the providers that has been installed inside the Airflow environment along with the version of it. Retrieves the exposed paths.</p>
<code>airflow info</code>

<h2>Airflow DB Initialization</h2>
<p>Used when just the airflow is installed and it's necessary to initialize the metadata Database. It tipically runs only at once.</p>
<code>airflow db init</code>

<h2>Airflow Users creation</h2>
<p>Used to create new users. It's possible to set the role, first name, last name, email and password.</p>
<code>airflow users create -e email@email.com -f first_name -l last_name -u username -p password -r role</code>

<h2>Add a role to a user</h2>
<p>It's possible to add an existing or custom role to an existing user.</p>
<code>airflow users add-role -e email@email.com -r role</code>

<h2>Run a standalone Airflow</h2>
<p>With this command it's possible to run the DB, the Airflow webserver and the scheduler all at once. (for development environment only)</p> 
<code>airflow standalone</code>

<h2>Discover the Airflow version</h2>
<p>Helpful for debbuging.</p> 
<code>airflow version </code>

<h2>Airflow config list</h2>
<p>Gives all the configuration settings list of the airflow installed .</p> 
<code>airflow config list</code>
<p>It's possible to find some specific configurations, such as the Airflow parallelism informations.</p>
<code>airflow config list | grep parallelism</code>

<h2>Airflow Cheat Sheet</h2>
<p>Gives a cheat sheet of airflow commands. basically all commands summarized.</p> 
<code>airflow cheat-sheet</code> 

<h2>Airflow Task Testing</h2>
<p>Ensuring the reliability and accuracy of tasks within your DAG is crucial. Testing is vital in achieving this, allowing you to validate task functionality, identify potential issues, and maintain data integrity before running the DAG or pushing it into production.</p> 
<code>airflow tasks test (dag_id) (task_id) (logical_date)</code>
<p>
This command runs a task without checking for dependencies or recording its state in the database. For example, if the task pushes an XCOM, the XCOM won't be created with that command</p>

<h2>Backfill</h2>
<p>The backfilling process is only available through the CLI or the API.</p> 
<h5>CLI</h5>
<code>airflow dags --dag-id dag_id backfill --end-date YYYY-MM-DD --start-date YYYY-MM-DD</code>
<h5>API</h5>

<p>A DAG that receives the start date and end date to run the BashOperator. The parameters could be sent through the Webserver UI, as a dictionary.</p>
<code>
{"dag_id": "example_dag_basic",
"date_start": 20230401, "date_end": 20230405}
</code>