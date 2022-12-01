from datetime import datetime, timedelta
from textwrap import dedent
import airflow
import pendulum
from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator



local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

init_dag = DAG(
    dag_id = 'sixdogma_hdfs_2',
    default_args = init_args,
    start_date = datetime(2022, 12, 1, 12, tzinfo=local_tz),
    schedule_interval = '@hourly'
)

local_dir = '/home/sixdogma/test/test.txt'
hdfs_dir = '/sixdogma_project'

input_file = BashOperator(
    task_id = 'input_file',
    bash_command = f'/usr/local/hadoop/bin/hdfs dfs -copyFromLocal -d {local_dir} {hdfs_dir}',
    dag = init_dag
)