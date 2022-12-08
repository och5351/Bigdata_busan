##### IMPORT PACKAGES #####
import time
import datetime
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

from slack_alert import SlackAlert


##### AIRFLOW BASIC SETTINGS #####
slack = SlackAlert('#airflow', 'xoxb-4187085457398-4480372543219-DX3L3m1TlcvH1DUpJO83vZOW')

local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

hook_flask = SSHHook(ssh_conn_id = 'ssh_flask', key_file='/home/sixdogma/.ssh/id_rsa')
hook_hadoop = SSHHook(ssh_conn_id = 'ssh_hadoop', key_file='/home/sixdogma/.ssh/id_rsa')

with DAG(
    dag_id = 'IMAGE_BAD_schedule',
    start_date = datetime(2022, 12, 8, 19, tzinfo=local_tz),
    schedule_interval = '0 21 * * *',
    default_args = init_args,
    on_success_callback=slack.success_msg,
    on_failure_callback=slack.fail_msg
) as dag:


##### MAKE DAGS #####
### 1. GET FILES from FLASK SERVER to HADOOP SERVER
# flask 폴더가 완전히 지워지면 안 되기 때문에 cat.jfif 제외
    flask_to_hadoop = SSHOperator(
        task_id = 'flask_to_hadoop',
        ssh_hook = hook_flask,
        command = 'scp -r /home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/images/bad/`ls /home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/images/bad/ | grep -v cat.jfif` root@35.75.77.128:/home/ubuntu/get_badimg'
    )

### 2. EMPTY OUT DIRECTORY in FLASK SERVER
# flask 폴더가 완전히 지워지면 안 되기 때문에 cat.jfif 제외
    empty_out_flask = SSHOperator(
        task_id = 'empty_out_flask',
        ssh_hook = hook_flask,
        command = 'sudo rm -r /home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/images/bad/`ls /home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/images/bad/ | grep -v cat.jfif`'
    )

### 3. GET FILES from HADOOP SERVER to HDFS
    hadoop_to_hdfs = SSHOperator(
        task_id = 'hadoop_to_hdfs',
        ssh_hook = hook_hadoop,
        command = '/usr/local/hadoop/bin/hdfs dfs -put /home/ubuntu/get_badimg/* /imgs/bad'
    )

### 4. EMPTY OUT DIRECTORY in HADOOP SERVER
    empty_out_hadoop = SSHOperator(
        task_id = 'empty_out_hadoop',
        ssh_hook = hook_hadoop,
        command = 'rm -r /home/ubuntu/get_badimg/*'
    )

### SET TASK FLOW
    (
        flask_to_hadoop
        >> empty_out_flask
        >> hadoop_to_hdfs
        >> empty_out_hadoop
    )