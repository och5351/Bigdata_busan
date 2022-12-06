from datetime import datetime, timedelta
from textwrap import dedent
import pendulum
import airflow

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.utils.decorators import apply_defaults
from hdfs import HdfsError, InsecureClient

from typing import Any, Optional
import logging
import socket
import requests


####### AIRFLOW 기초 설정 #######
local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}


####### 경로 관련 #######
webhdfs_conn_id = 'webhdfs_default'
hdfs_dir = '/sixdogma_project'
local_dir = '/home/sixdogma/test/test.txt'


####### 함수 만들기 #######
def UploadHdfs(hdfs, local, **kwargs):
    client_hdfs = InsecureClient('http://3.112.187.213' + ':9870')
    client_hdfs.upload(hdfs_path=hdfs, local_path=local, n_threads=1, overwrite=True)


####### DAG 만들기 #######
with DAG(
    dag_id = 'hdfs_test_test',
    start_date = datetime(2022, 12, 1, 20, tzinfo=local_tz),
    schedule_interval = '@hourly',
    default_args = init_args,
    catchup = False
) as dag:

    uploadhdfs = PythonOperator(
        task_id = 'uploadhdfs',
        python_callable = UploadHdfs,
        op_kwargs = {'hdfs': hdfs_dir, 'local': local_dir}
    )