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

local_dir = '/home/sixdogma/test/test.txt'

with DAG(
    dag_id = 'hdfs_test',
    start_date = datetime(2022, 12, 1, 14, tzinfo=local_tz),
    schedule_interval = '@hourly',
    default_args = init_args,
    catchup = False,
) as dag:

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
    )

    ### task 순서 설정
    (
        is_webhdfs_available
        >> webhdfs_operator
    )