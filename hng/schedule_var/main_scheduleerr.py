'''
1. 패키지 import
'''
from datetime import datetime, timedelta
from textwrap import dedent
import airflow
import pendulum
from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

from slack_alert import SlackAlert


'''
2. 슬랙 알람 설정
'''
slack = SlackAlert('#airflow', 'xoxb-4187085457398-4480372543219-DX3L3m1TlcvH1DUpJO83vZOW')

def print_result(**kwargs):
    r = kwargs['task_instance'].xcom_pull(key='result_msg')
    print('message : ', r)


'''
3. Airflow DAG 설정 및 선언
'''
local_tz = pendulum.timezone('Asia/Seoul')

init_args = {
    'owner' : 'airflow'
}

init_dag = DAG(
    dag_id = 'ERROR_schedule',
    default_args = init_args,
    start_date = datetime(2022, 12, 8, 19, tzinfo=local_tz),
    schedule_interval = '30 19 * * *',
    on_success_callback=slack.success_msg,
    on_failure_callback=slack.fail_msg
)


'''
4. 에러로트 처리 함수화
'''
### 1. err_PreProcessing : CSV 파일 하나당 전처리하는 코드
def err_PreProcessing(main_dir, err_dir):
    ## (1) 필요한 package import
    # 기본적인 패키지
    import pandas as pd
    import numpy as np
    import pyarrow
    from datetime import datetime

    # 디렉토리 관련 패키지
    import os
    import glob
    import natsort

    ## (2) 데이터프레임 생성하는 코드
    df = pd.read_csv(os.path.join(main_dir, err_dir), engine='pyarrow')

    ## (3) 데이터프레임 전처리하는 코드
    df.rename(columns = {'0':'Date', '1':'FailureLot1', '2':'FailureLot2'}, inplace=True)
    
    ## (4) 결과물 df 리턴
    return df

### 2. err_Merging : csv파일 전부 merge하고 정리하는 코드
def err_Merging(file_dir):
    ## (1) 필요한 package import
    # 기본적인 패키지
    import pandas as pd
    import numpy as np
    import pyarrow
    from datetime import datetime

    # 디렉토리 관련 패키지
    import os
    import glob
    import natsort

    ## (2) 주어진 경로에서 파일들 불러내기
    errlist = natsort.natsorted(os.listdir(file_dir))
    errlist = [file for file in errlist if file.endswith('.csv')]

    ## (3) 미리 빈 데이터프레임 생성하기
    err_df = pd.DataFrame()

    ## (4) 전처리 코드 실행 : 모든 파일에 대해 반복문 돌리기
    for i in range(len(errlist)):
        df = err_PreProcessing(file_dir, errlist[i])
        df = df[['Date', 'FailureLot1', 'FailureLot2']]
        err_df = pd.concat([err_df, df], axis=0)

    ## (5) 결과물 var_df 리턴
    return err_df

### 3. err_InputSQL : SQL Alchemy 실행시키고 집어넣는 코드
def err_InputSQL(root_dir, **kwargs):
    ## (1) 필요한 package import
    # MySQL 관련 패키지
    import MySQLdb
    import mysql.connector

    # SQL Alchemy 관련 패키지 1
    import sqlalchemy
    from sqlalchemy import create_engine

    # SQL Alchemy 관련 패키지 2
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Table, MetaData
    from sqlalchemy import insert, update

    ## (2) SQL Alchemy로 MySQL에 연결
    url = 'mysql+mysqldb://sixdogma:Poiu0987*@13.113.12.130:3306/Analysis'
    engine = sqlalchemy.create_engine(url, encoding='utf-8', echo=True)

    ## (3) Merge한 데이터프레임 소환
    err_df = err_Merging(root_dir)

    ## (4) to_sql()로 MySQL에 넣어주기
    err_type = {'Date'    : sqlalchemy.types.DATE(),
                'FailureLot1' : sqlalchemy.types.INT(),
                'FailureLot2' : sqlalchemy.types.INT()
                }
    err_df.to_sql(name='ERROR', con=engine, if_exists='append', index=False, dtype=err_type)


'''
5. 오퍼레이터 코드 작성
'''
# err_prepro = PythonOperator(
#     task_id = 'err_prepro',
#     python_callable = err_PreProcessing,
#     dag = init_dag
# )

# err_merging = PythonOperator(
#     task_id = 'err_merging',
#     python_callable = var_Merging,
#     dag = init_dag
# )

err_inputsql = PythonOperator(
    task_id = 'err_inputsql',
    python_callable = err_InputSQL,
    op_kwargs = {'root_dir': '/home/sixdogma/testinput/error'},
    dag = init_dag
)

msg = PythonOperator(
    task_id = 'msg',
    python_callable = print_result,
    dag = init_dag
)


'''
6. DAG task 순서 설정
'''
err_inputsql >> msg

# err_prepro >> err_merging >> err_inputsql
# 실제로 작동하는 함수는 err_InputSQL이고 나머지는 그 함수를 작동하기 위한 함수이므로
# 실질적으로 err_InputSQL 하나만 돌리면 된다!