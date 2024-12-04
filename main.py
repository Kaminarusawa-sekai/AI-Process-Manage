import csv

from datetime import datetime, timedelta
import types

# 定义默认参数
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 创建DAG对象
dag = DAG(
    'dynamic_dag_example',
    default_args=default_args,
    description='A dynamic DAG example with dynamic functions and XCom',
    schedule_interval=timedelta(days=1),
)

# 动态生成任务函数
functions = {}
with open('tasks.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        function_name = row['function_name']
        function_code = row['function_code']
        exec(function_code, globals())
        functions[function_name] = globals()[function_name]

# 读取任务列表
tasks = []
with open('tasks.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tasks.append(row)

# 创建任务对象并设置依赖关系
task_objs = {}
for task in tasks:
    task_name = task['task_name']
    function_name = task['function_name']
    dependencies = task['dependencies'].split(',')
    params = eval(task['params'])  # 将字符串转换为字典

    # 创建任务对象
    task_obj = PythonOperator(
        task_id=task_name,
        python_callable=functions[function_name],
        op_kwargs=params,
        provide_context=True,
        dag=dag,
    )
    task_objs[task_name] = task_obj

    # 设置依赖关系
    for dep in dependencies:
        if dep:  # 忽略空字符串
            task_objs[dep] >> task_obj

# 动态生成的DAG会自动注册到Airflow中