##### IMPORT PACKAGES #####
from datetime import datetime, timedelta
from textwrap import dedent
import pendulum
import airflow
from airflow.utils.dates import days_ago

# from airflow import DAG
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook


##### AIRFLOW BASIC SETTINGS #####

local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

# 나중에 hook_default -> hook_flask
# ssh_conn_id : 'ssh_default' -> 'ssh_flask' 로 변경
hook_default = SSHHook(ssh_conn_id = 'ssh_default', key_file='/home/sixdogma/.ssh/id_rsa')
hook_hadoop = SSHHook(ssh_conn_id = 'ssh_hadoop', key_file='/home/sixdogma/.ssh/id_rsa')

with DAG(
    dag_id = 'img_scheduling',
    start_date = datetime(2022, 12, 6, 17, tzinfo=local_tz),
    schedule_interval = '5 * * * *',
    default_args = init_args
) as dag:


##### MAKE DAGS #####
### MAKE DIRECTORY NAME TODAY'S DATE in HADOOP SERVER
    mkdir_today = SSHOperator(
        task_id = 'mkdir_today',
        ssh_hook = hook_hadoop,
        command = 'mkdir /home/ubuntu/put_to_hdfs/{}',
    )

### from FLASK SERVER to HADOOP SERVER
    flask_to_hadoop = SSHOperator(
        task_id = 'flask_to_hadoop',
        ssh_hook = hook_default,
        command = 'scp -r /home/sixdogma/test/test2 root@35.75.77.128:/home/ubuntu/put_to_hdfs/{}'
    )

### from HADOOP SERVER to HDFS
    hadoop_to_hdfs = SSHOperator(
        task_id = 'hadoop_to_hdfs',
        ssh_hook = hook_hadoop,
        command = 'hdfs dfs -put /home/ubuntu/put_to_hdfs/{} /sixdogma/imgs/{}'
    )

### REMOVE DIRECTORY in HADOOP SERVER
    hadoop_remove = SSHOperator(
        task_id = 'hadoop_remove',
        ssh_hook = hook_hadoop,
        command = 'rm -r /home/ubuntu/put_to_hdfs/{}'
    )

### SET TASK FLOW
    (
        mkdir_today
        >> flask_to_hadoop
        >> hadoop_to_hdfs
        >> hadoop_remove
    )  