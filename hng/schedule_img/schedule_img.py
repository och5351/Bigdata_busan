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



webhdfs_operator = WebHDFSOperator(
    task_id = 'webhdfs_operator',
    webhdfs_conn_id = 'webhdfs_default',
    source = f'{local_dir}',   # source: local path of file or folder
    destination = f'{hdfs_dir}',   # destination: HDFS path target
    dag = init_dag
)

# t1 = BashOperator(
#     task_id = 'move_test',
#     bash_command = f'/usr/local/hadoop/bin/hdfs dfs -copyFromLocal -d {local_dir} {hdfs_dir}',
#     dag = init_dag
# )

# copy good image data from web directory to HDFS
# t1 = BashOperator(
#     task_id = 'move_good',
#     bash_command = f'/usr/local/hadoop/bin/hdfs dfs -copyFromLocal -d {local_good_dir} {hdfs_good_dir}',
#     dag = init_dag
# )

# copy bad image data from web directory to HDFS
# t2 = BashOperator(
#     task_id = 'move_bad',
#     bash_command = f'/usr/local/hadoop/bin/hdfs dfs -copyFromLocal -d {local_bad_dir} {hdfs_bad_dir}',
#     dag = init_dag
# )



# t1 >> t2



# 다른 방법
# is_hdfs_available = WebHdfsSensor(
#     task_id = 'is_hdfs_available',
#     webhdfs_conn_id = 'webhdfs_default'
# )

# webhdfs_operator = WebHDFSOperator(
#     task_id = 'webhdfs_operator',
#     webhdfs_conn_id = 'webhdfs_default',
#     source = f'{local_good_dir}',   # source: local path of file or folder
#     destination = f'{hdfs_good_dir}'   # destination: HDFS path target
# )



# is_hdfs_available >> webhdfs_operator