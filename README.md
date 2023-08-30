<h1>Airflow Study Repo</h1>

<h2>Airflow setup</h2>
<h3>With Docker</h3>
<ol>
<li>Install Docker;</li>
<li>Fetch Docker-compose file: <code>curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.0/docker-compose.yaml'</code></li>
<li>.env file: <code>echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env</code></li>
<li>docker-compose init: <code>docker-compose up airflow-init</code></li>
<li>docker-compose up: <code>docker-compose up</code></li>
</ol>
