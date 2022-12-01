from datetime import datetime, timedelta
from textwrap import dedent
import airflow
import pendulum
from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hdfs.sensors.web_hdfs import WebHdfsSensor

from webhdfs_operator import WebHDFSOperator
from webhdfs_hooks import WebHDFSHook



local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

init_dag = DAG(
    dag_id = 'sixdogma_hdfs',
    default_args = init_args,
    start_date = datetime(2022, 11, 30, 17, tzinfo=local_tz),
    schedule_interval = '@hourly'
)



local_dir = '/home/sixdogma/test/test.txt'
hdfs_dir = '/sixdogma_project'
# local_good_dir = '/home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/images/good'
# local_bad_dir = '/home/ubuntu/projects/Bigdata_busan/web/project/dogma/static/images/bad'

# hdfs_good_dir = '/sixdogma_project/imgs/good'
# hdfs_bad_dir = '/sixdogma_project/imgs/bad'



is_webhdfs_available = WebHdfsSensor(
    task_id = 'is_webhdfs_available',
    webhdfs_conn_id = 'webhdfs_default' 
)

webhdfs_operator = WebHDFSOperator(
    task_id = 'webhdfs_operator',
    webhdfs_conn_id = 'webhdfs_default',
    source = local_dir,   # source: local path of file or folder
    destination = hdfs_dir,   # destination: HDFS path target
    dag = init_dag
)

is_webhdfs_available >> webhdfs_operator