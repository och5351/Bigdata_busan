from datetime import datetime, timedelta
from textwrap import dedent
import airflow
import pendulum
# from airflow import DAG

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from webhdfs_sensor import WebHDFSSensor
from webhdfs_hook import WebHDFSHook
from webhdfs_operator import WebHDFSOperator



local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

init_dag = DAG(
    dag_id = 'hdfs_test',
    default_args = init_args,
    start_date = datetime(2022, 12, 1, 14, tzinfo=local_tz),
    schedule_interval = '@hourly'
)



local_dir = '/home/sixdogma/test/test.txt'
# hdfs_dir = 'http://3.112.187.213:9870/webhdfs/v1/sixdogma_project/'



### 작동 성공
is_webhdfs_available = WebHDFSSensor(
    task_id = 'is_webhdfs_available',
    webhdfs_conn_id = 'webhdfs_default',
    filepath = '/sixdogma_project'
)

### 에러 발생
webhdfs_operator = WebHDFSOperator(
    task_id = 'webhdfs_operator',
    webhdfs_conn_id = 'webhdfs_default',
    source = local_dir,   # source: local path of file or folder
    destination = '/sixdogma_project',   # destination: HDFS path target
    dag = init_dag
)

is_webhdfs_available >> webhdfs_operator