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
    dag_id = 'VARIABLE_schedule',
    default_args = init_args,
    start_date = datetime(2022, 12, 8, 19, tzinfo=local_tz),
    schedule_interval = '0 19 * * *',
    on_success_callback=slack.success_msg,
    on_failure_callback=slack.fail_msg
)


'''
4. 공정환경변수 처리 함수화
'''
### 1. var_PreProcessing : CSV 파일 하나당 전처리하는 코드
def var_PreProcessing(main_dir, var_dir):
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
    df = pd.read_csv(os.path.join(main_dir, var_dir), engine='pyarrow')

    ## (3) csv 파일명으로부터 'Date' 컬럼 만들어주기
    df['Date'] = '-'.join(var_dir.split('-')[-1].split('.')[:-1])

    ## (4) 'Time' 컬럼 전처리
    adj_time = list()
    for time in df['Time']:
        tmp = time.split(':')
        if tmp[0].split(' ')[0] == '오후':
            tmp[0] = str(int(tmp[0].split(' ')[-1]) + 12)
        else:
            tmp[0] = tmp[0].split(' ')[-1]
        tmp = ':'.join(tmp).split('.')[0]
        adj_time.append(tmp)
    df['Time'] = adj_time

    ## (5) 스케줄링을 위해서는 유니크 컬럼이 필요
    # 'Date'와 'Time' 합쳐서 'DateTime' 컬럼 만들기
    df['DateTime'] = df['Date'] + ' ' + df['Time']
    
    ## (6) 결과물 df 리턴
    return df

### 2. var_Merging : csv파일 전부 merge하고 정리하는 코드
def var_Merging(file_dir):
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
    varlist = natsort.natsorted(os.listdir(file_dir))
    varlist = [file for file in varlist if file.endswith('.csv')]

    ## (3) 미리 빈 데이터프레임 생성하기
    var_df = pd.DataFrame()

    ## (4) 전처리 코드 실행 : 모든 파일에 대해 반복문 돌리기
    for i in range(len(varlist)):
        df = var_PreProcessing(file_dir, varlist[i])
        df = df[['Index', 'DateTime', 'Date', 'Time', 'Lot', 'pH', 'Temp', 'Voltage']]
        var_df = pd.concat([var_df, df], axis=0)
        
    ## (5) 필요없는 'Index' 컬럼 삭제
    var_df.drop(columns=['Index'], inplace=True)

    ## (6) 결과물 var_df 리턴
    return var_df

### 3. var_InputSQL : SQL Alchemy 실행시키고 집어넣는 코드
def var_InputSQL(root_dir, **kwargs):
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
    var_df = var_Merging(root_dir)

    ## (4) to_sql()로 MySQL에 넣어주기
    var_type = {'DateTime':sqlalchemy.types.DATETIME(),
                'Date':sqlalchemy.types.DATE(),
                'Time':sqlalchemy.types.TIME(),
                'Lot':sqlalchemy.types.INT(),
                'pH':sqlalchemy.types.FLOAT(),
                'Temp':sqlalchemy.types.FLOAT(),
                'Voltage':sqlalchemy.types.FLOAT()
                }

    var_df.to_sql(name='VARIABLE', con=engine, if_exists='append', index=False, dtype=var_type)


'''
5. 오퍼레이터 코드 작성
'''
# var_prepro = PythonOperator(
#     task_id = 'var_prepro',
#     python_callable = var_PreProcessing,
#     dag = init_dag
# )

# var_merging = PythonOperator(
#     task_id = 'var_merging',
#     python_callable = var_Merging,
#     dag = init_dag
# )

var_inputsql = PythonOperator(
    task_id = 'var_inputsql',
    python_callable = var_InputSQL,
    op_kwargs = {'root_dir': '/home/sixdogma/testinput/variable'},
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
var_inputsql >> msg

# var_prepro >> var_merging >> var_inputsql
# 실제로 작동하는 함수는 var_InputSQL이고 나머지는 그 함수를 작동하기 위한 함수이므로
# 실질적으로 var_InputSQL 하나만 돌리면 된다!