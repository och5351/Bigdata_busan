'''
##### Apache HDFS Connection

### Host : local, yarn, or an URL. For Web HDFS Hook it is possible to specify multiple hosts as a comma-seperated list.

### Port : Specify the port in case of host be an URL.

### Login : Effective user for HDFS operations.

### Extra(optional):
## autoconfig : Default value is bool:False.
# Use snakebite's automatically configured client.
# This HDFSHook implementation requires snakebite.

## hdfs_namenode_principal :
# Specifies the Kerberos principal to use for HDFS.

## use_ssl : By default is set to false

## verify : How to verify SSL.
# requests.get('https~', verify='/path/to/certfile')
# s = request.Session()
# s.verify = '/path/to/certfile'



##### SSH Connection

### Host : The remote host to connect.

### Username(optional) : The Username to connect to the remote_host.

### Password(optional) : Specify the password of the username

### Port(optional) : Port of remost host to connect. Default is 22

### Extra(optional) :
## no_host_key_check : Default is true, ssh will automatically add new host keys to the user known host files.

## allow_host_key_change : set to true if you want to allow connecting to hosts that has host key changed.

## host_key : 
'''


from datetime import datetime, timedelta
from textwrap import dedent
import airflow
import pendulum
from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook



local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

init_dag = DAG(
    dag_id = 'sixdogma_hdfs',
    default_args = init_args,
    start_date = datetime(2022, 11, 29, tzinfo=local_tz),
    schedule_interval = '@daily'
)



local_dir = f'/tmp/data/{today_EDT_str}'
hdfs_dir = '/sixdogma_project/imgs'



is_hdfs_available = WebHdfsSensor(
    task_id = 'is_hdfs_available',
    webhdfs_conn_id = 'webhdfs_default'
)

webhdfs_operator = WebHDFSOperator(
    task_id = 'webhdfs_operator',
    webhdfs_conn_id = 'webhdfs_default',
    source = f'',   # source: local path of file or folder
    destination = f''   # destination: HDFS path target
)



is_hdfs_available >> webhdfs_operator