<h1>Airflow Dynamic Tasks</h1>

<h2>Topics</h2>
<ul>
<li>Difference Between Normal and Dynamic Tasks;</li>
</ul>

<h2>Normal vs. Dynamic Tasks</h2>
<div style="text-align: center; ">
<table border="1">
        <tr style="color: white; background-color: black;">
            <th>Common</th>
            <th>Dynamic</th>
        </tr>
        <tr>
            <td>Tasks are generated when the DAG file is parsed</td>
            <td>Tasks are generated dynamically at runtime</td>
        </tr>
        <tr>
            <td>To change the number of tasks the DAG code needs to be changed</td>
            <td>The number of tasks can change without code changes</td>
        </tr>
    </table>
</div>

<h2>Use cases</h2>
<h3>ETL</h3>
<ul>
    <li>Create one task per file in an S3 bucket or record returned</li>
    <li>Using .map to selectively skip processing records at runtime</li>
</ul>
<h3>ML</h3>
<ul>
    <li>Train models with differents sets of hyperparameters with one task per set</li>
    <li>Use a cross product to train a model with all possible combinations of hyperparameters</li>
</ul>

<h2>Benefits</h2>
<ul>
    <li>Expands use cases of traditional operators;</li>
    <li>Atomicity</li>
    <li>Observability: know exactly which mapped task failed or were skipped;</li>
    <li>Preserve detailed history of task runs</li>
    <li>Can replace some instances of dynamic DAGs</li>
</ul>

<h2>Basic concepts</h2>
<ul>
    <li>A dynamically mapped task is defined instantiating one operator with</li>
        <ul>
            <li>Static parameters in <code>.partial()</code></li>
            <li>Dynamic parameters in <code>.expand()</code> or <code>.expand_kwargs()</code></li>
        </ul>
    <li>Only at runtime will Airflow compute how many mapped task instances are created</li>
    <li>You can use the output of an upstream task to map over</li>
    <li>You can map over multiple parameters</li>
    <li>Parameters that are needed by the scheduler (BaseOperator) aren't mappable</li>
</ul>
<h3><code>.expand()</code> vs. <code>.expand_kwargs()</code></h3>
<h4>.expand()</h4>
<ul>
    <li>Only accepts keywords arguments</li>
    <li>Can take several keyword arguments and will create a cross product.</li>
</ul>
<code>
    
    kwarg1=[1,2,3], kwarg2=[10, 20, 30]
</code>
<p>Will result in 9 mapped task instances.</p>
<h4>.expand_kwargs()</h4>
<ul>
    <li>Only accepts a list[dict]</li>
    <li>Used to pass sets of keyword arguments.</li>
</ul>
<code>

    [
        {"kwarg1": 1, "kwarg2": 10},
        {"kwarg1": 2, "kwarg2": 20},
        {"kwarg1": 3, "kwarg2": 30}
    ]
</code>
<p>Will result in 3 mapped task instances.</p>

<h3><code>.zip()</code></h3>
<p>The zip() built-in Python function is helpful when you have an operator that takes several positional arguments</p>
<code>zip([1,2], [a,b], {x,y}) => (1, a, x), (2, b, y)</code>
<p>You can use Python zip objects or zip
together outputs from upstream tasks:</p>
<code>

    my_task one().zip(
        my_task_two(), my_task_three()
    )
</code>