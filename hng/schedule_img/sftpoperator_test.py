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

from airflow.providers.sftp.sensors.sftp import SFTPSensor
from airflow.providers.sftp.operators.sftp import SFTPOperator


##### AIRFLOW BASIC SETTINGS #####

local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id = 'sftp_test',
    start_date = datetime(2022, 12, 6, 15, tzinfo=local_tz),
    schedule_interval = '5 * * * *',
    default_args = init_args
) as dag:

##### AIRFLOW TASK DEFINITION #####
### 1. CHECK CONNECTION
    sftp_sensor = SFTPSensor(
        task_id = 'sftp_sensor',
        ssh_conn_id = 'ssh_default',
        path = '/home/sixdogma/test/test2'
    )

### 2. FROM FLASK WEB SERVER TO HADOOP WEB SERVER
    put_in_server = SFTPOperator(
        task_id = 'put_in_server',
        ssh_conn_id = 'ssh_default',
        local_filepath = '/home/sixdogma/test/test2',
        remote_filepath = '/home/ubuntu/testfolder/',
        operation = 'put',
        confirm = True,
        create_intermediate_dirs = True
    )

### 3. FROM HADOOP WEB SERVER TO HADOOP HDFS

### 4. TASK FLOW
    (
        sftp_sensor
        >> put_in_server
    )