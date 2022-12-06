import json
from datetime import datetime
from airflow import DAG, macros
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
 
import sqlalchemy
import pandas as pd
 
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 1, 1, 11, 0),
    'schedule_interval': '0 11 * * *',
}
 
dag = DAG(
    dag_id= """ddongmin_220612_pipeline_subway_passenger_cnt""",
    default_args= default_args,
)



sql_task_delete_table = MySqlOperator(
    task_id= 't1_check_duplicate',
    mysql_conn_id= 'mysql_connection',
    sql= "DELETE FROM airflow_test_db.subway_table WHERE USE_DT = '{date}'".format(
    date='{{ (execution_date - macros.timedelta(days=3)).strftime("%Y-%m-%d") }}'),
    dag= dag,
)

get_api = SimpleHttpOperator(
    task_id= 't2_get_request_response',
    http_conn_id= 'http_subway',
    endpoint= '{date}'.format(
    date='{{ (execution_date - macros.timedelta(days=3)).strftime("%Y%m%d") }}'),
    method= 'GET',
    response_filter= lambda response: json.loads(response.text),
    log_response= True,
    dag= dag,
    )

def dataframe_to_sql(ti):
    # json preprocessing
    subway_json= ti.xcom_pull(task_ids=['t2_get_request_response'])
    subway_json_decode= subway_json[0]['CardSubwayStatsNew']['row'] 
    subway_json_normalize= pd.json_normalize(subway_json_decode)
    
    # db info
    user_name= ''
    pass_my  = ''
    host_my  = ''
    db_name  = ''
    
    # to_sql
    connection= sqlalchemy.create_engine(f"mysql+mysqlconnector://{user_name}:{pass_my}@{host_my}/{db_name}")
    table_name= 'subway_table'
    subway_json_normalize.to_sql(name      = table_name
                                ,con       = connection
                                ,index     = False
                                ,if_exists = 'append')
 
df_to_sql = PythonOperator(
    task_id= 't3_pd_to_sql',
    python_callable= dataframe_to_sql,
    dag= dag
)



sql_task_delete_table >> get_api >> df_to_sql