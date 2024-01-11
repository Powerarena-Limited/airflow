import random
from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_kubernetes_dag',
    default_args=default_args,
    description='A simple Airflow DAG with Kubernetes Executor',
    schedule_interval=timedelta(days=1),
)

random_number = random.randint(0, 60)
print("@22", random_number)

task_hello = KubernetesPodOperator(
    task_id='hello_task',
    name='hello-pod',
    image='busybox',
    cmds=['sh', '-c', f'time sleep {random_number}'],
    namespace='airflow',  # Change this according to your namespace
    dag=dag,
)

bash_task = BashOperator(
    task_id='run_bash_command',
    bash_command=f'echo "Hello, Airflow?! {random_number}"',  # Replace with your actual Bash command
    dag=dag,
)

task_hello >> bash_task