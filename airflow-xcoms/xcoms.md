<h1>Airflow XComs</h1>

<h2>Topics</h2>
<ul>
<li>What are XComs?</li>
<li>Custom XComs Backends</li>
<li>Working with Custom XCom Backends in Containers</li>
</ul>

<h2>What are XComs?</h2>
<p>XComs (short for “cross-communications”) are a mechanism that let Tasks talk to each other, as by default Tasks are entirely isolated and may be running on entirely different machines.</p>
<p>An XCom is identified by a <code>key</code> (essentially its name), as well as the <code>task_id</code> and <code>dag_id</code> it came from. They can have any (serializable) value, but they are only designed for small amounts of data; do not use them to pass around large values, like dataframes.</p>
<p>XComs are explicitly “pushed” and “pulled” to/from their storage using the <code>xcom_push</code> and <code>xcom_pull</code> methods on Task Instances. Many operators will auto-push their results into an XCom key called <code>return_value</code> if the <code>do_xcom_push</code> argument is set to True (as it is by default), and <code>@task</code> functions do this as well.</p>
<p><code>xcom_pull</code> defaults to using this key if no key is passed to it, meaning it’s possible to write code like this:</p>
<code>

    # Pulls the return_value XCOM from "pushing_task"
    value = task_instance.xcom_pull(task_ids='pushing_task')
</code>
<p>XComs are a relative of Variables, with the main difference being that XComs are per-task-instance and designed for communication within a DAG run, while Variables are global and designed for overall configuration and value sharing.</p>

<h2>Custom XComs Backends</h2>
<p>The XCom system has interchangeable backends, and you can set which backend is being used via the xcom_backend configuration option.</p>
<p>If you want to implement your own backend, you should subclass BaseXCom, and override the serialize_value and deserialize_value methods.</p>
<p>There is also an orm_deserialize_value method that is called whenever the XCom objects are rendered for UI or reporting purposes; if you have large or expensive-to-retrieve values in your XComs, you should override this method to avoid calling that code (and instead return a lighter, incomplete representation) so the UI remains responsive.</p>