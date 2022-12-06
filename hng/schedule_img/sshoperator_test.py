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
    dag_id = 'ssh_realtest',
    start_date = datetime(2022, 12, 6, 17, tzinfo=local_tz),
    schedule_interval = '5 * * * *',
    default_args = init_args
) as dag:

##### MAKE DAGS #####
### from FLASK SERVER to HADOOP SERVER
    ssh_default = SSHOperator(
        task_id = 'ssh_default',
        ssh_hook = hook_default,
        command = 'scp /home/sixdogma/test/test2 root@35.75.77.128:/home/ubuntu/testfolder'
        )

### from HADOOP SERVER to HDFS
    ssh_hadoop = SSHOperator(
        task_id = 'ssh_hadoop',
        ssh_hook = hook_hadoop,
        command = 'hdfs dfs -put /home/ubuntu/testfolder/test2 /test/test2'
        )

### SET TASK FLOW
    (
        ssh_default
        >> ssh_hadoop
    )