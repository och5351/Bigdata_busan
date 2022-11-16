'''
1. 패키지 import
'''
# 기본 패키지 import
import pandas as pd
import numpy as np
import pyarrow
from datetime import datetime

# 디렉토리 관련 패키지
import os
import glob
import natsort

# MySQL 관련 패키지
import MySQLdb
import mysql.connector

# SQL Alchemy 관련 패키지 1
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import *
from sqlalchemy.types import *

# SQL Alchemy 관련 패키지 2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from sqlalchemy import insert, update

# Airflow 패키지
import airflow
import pendulum
from airflow import DAG
from airflow.operators.mysql_operator import MySQLOperator
from airflow.operators.python_operator import PythonOperator


'''
2. Airflow DAG 설정 및 선언
'''
local_tz = pendulum.timezone('Asia/Seoul')
init_args = {
    'owner' : 'airflow',
    'start_date' : datetime(2022, 11, 17, 0, tzinfo=local_tz),
    'schedule_interval' : '0 0 * * *'
}

init_dag = DAG(
    dag_id = 'sixdogma_chromate',
    default_args = init_args,
)


'''
3. 함수화
'''
# 1. PreProcessing : CSV 파일 하나당 전처리하는 코드
def PreProcessing(main_dir, var_dir):
    # (1) 데이터프레임 생성하는 코드
    df = pd.read_csv(os.path.join(main_dir, var_dir), engine='pyarrow')

    # (2) csv 파일명으로부터 'Date' 컬럼 만들어주기
    df['Date'] = '-'.join(var_dir.split('-')[-1].split('.')[:-1])

    # (3) 'Time' 컬럼 전처리
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

    # (4) 스케줄링을 위해서는 유니크 컬럼이 필요
    # 'Date'와 'Time' 합쳐서 'DateTime' 컬럼 만들기
    df['DateTime'] = df['Date'] + ' ' + df['Time']
    
    # (5) 결과물 df 리턴
    return df

# 2. Merging : csv파일 전부 merge하고 정리하는 코드
def Merging(file_dir):
    # (1) 주어진 경로에서 파일들 불러내기
    varlist = natsort.natsorted(os.listdir(file_dir))
    varlist = [file for file in varlist if file.endswith('.csv')]

    # (2) 미리 빈 데이터프레임 생성하기
    var_df = pd.DataFrame(columns=['Index', 'DateTime', 'Date', 'Time', 'Lot', 'pH', 'Temp', 'Voltage'])

    # (3) 전처리 코드 실행 : 모든 파일에 대해 반복문 돌리기
    for i in range(len(varlist)):
        df = PreProcessing(file_dir, varlist[i])
        df = df[['Index', 'DateTime', 'Date', 'Time', 'Lot', 'pH', 'Temp', 'Voltage']]
        var_df = pd.concat([var_df, df], axis=0)
        
    # (4) 필요없는 'Index' 컬럼 삭제
    var_df.drop(columns=['Index'], inplace=True)

    # (5) 결과물 var_df 리턴
    return var_df

# 3. InputSQL : SQL Alchemy 실행시키고 집어넣는 코드
def InputSQL(root_dir):
    # (1) SQL Alchemy로 MySQL에 연결
    url = 'mysql+mysqldb://sixdogma:Poiu0987*@13.113.12.130:3306/Test'
    engine = sqlalchemy.create_engine(url, encoding='utf-8', echo=True)

    # (2) Merge한 데이터프레임 소환
    var_df = Merging(root_dir)

    # (3) to_sql()로 MySQL에 넣어주기
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
4. 함수화 확인
'''
# dir = r'C:\Users\admin\Desktop\FinalProject\chromate\chromate_data\variable\\'
# InputSQL(dir)


'''
5. 오퍼레이터 코드 작성
'''
df_to_sql = PythonOperator(
    task_id= 'pd_to_sql',
    python_callable = InputSQL,
    dag=init_dag
)