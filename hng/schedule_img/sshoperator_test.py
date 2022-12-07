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
hook_flask = SSHHook(ssh_conn_id = 'ssh_flask', key_file='/home/sixdogma/.ssh/id_rsa')
hook_hadoop = SSHHook(ssh_conn_id = 'ssh_hadoop', key_file='/home/sixdogma/.ssh/id_rsa')

with DAG(
    dag_id = 'ssh_flasktest',
    start_date = datetime(2022, 12, 6, 17, tzinfo=local_tz),
    schedule_interval = '5 * * * *',
    default_args = init_args
) as dag:

##### MAKE DAGS #####
### from FLASK SERVER to HADOOP SERVER
    ssh_flask = SSHOperator(
        task_id = 'ssh_default',
        ssh_hook = hook_flask,
        command = 'scp -r /home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/imgs root@35.75.77.128:/home/ubuntu/testfolder'
        )

### from HADOOP SERVER to HDFS
    ssh_hadoop = SSHOperator(
        task_id = 'ssh_hadoop',
        ssh_hook = hook_hadoop,
        # command = 'hdfs dfs -put /home/ubuntu/testfolder/test2 /test/test2'
        command = '/usr/local/hadoop/bin/hdfs dfs -put /home/ubuntu/testfolder/imgs /test/imgs'
        )

### SET TASK FLOW
    (
        ssh_flask
        >> ssh_hadoop
    )