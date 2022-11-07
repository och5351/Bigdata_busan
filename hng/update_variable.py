# 기본 패키지 및 py import
import pandas as pd
import numpy as np
import time
import datetime
from time import strftime

# 추가 패키지
import pyarrow
import pyspark
from pyspark.sql import SparkSession

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



'''
1. SQL Alchemy 연결
'''
# SQL Alchemy 연결 - 함수 형식으로 정의
def MySQL_connect(user, password, db, host, port=3306):
    url = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    engine = sqlalchemy.create_engine(url, encoding='utf-8', echo=True)
    return engine

engine = MySQL_connect('sixdogma', 'Poiu0987*', 'Anay', '54.250.124.140')

engine.execute("SET GLOBAL event_scheduler = ON;")



'''
csv 파일 경로 세팅 => 추후 linux file system 경로로 수정
'''
# var_dir : 공정환경변수 파일 기본 경로
var_dir = r'C:\Users\admin\Desktop\FinalProject\chromate\chromate_data\variable\\'
# varfilelist : 공정환경변수 파일 기본 경로 안의 csv 파일 목록들
varfilelist = natsort.natsorted(os.listdir(var_dir))
varfilelist = [file for file in varfilelist if file.endswith('.csv')]

# err_dir : 에러로트 파일 기본 경로
err_dir = r'C:\Users\admin\Desktop\FinalProject\chromate\chromate_data\error\\'
# errfilelist : 에러로트 파일 기본 경로 안의 csv 파일 목록들
errfilelist = natsort.natsorted(os.listdir(err_dir))
errfilelist = [file for file in errfilelist if file.endswith('.csv')]



'''
2. 전처리 함수 만들기
'''
# (1) csv 파일 하나 단위당 전처리하는 코드
def PreProcessing(root_dir, var_list):
    df = pd.read_csv(os.path.join(root_dir, var_list), engine='pyarrow')

    # (1)-1 csv 파일명으로부터 'Date' 컬럼 만들어주기
    df['Date'] = '-'.join(var_list.split('-')[-1].split('.')[:-1])

    # (1)-2 'Time' 컬럼 전처리 : 간단하게 할 수 있는 strftime, strptime 방법 찾아볼 것
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
    
    return df

# (2) csv 파일 전부 merge하고 정리하는 코드 
def MergeFrame(root_dir, var_list):
    # (2)-1 우선 row 하나로 데이터프레임 만들어놓고 거기에 merge해나간다
    var_df = PreProcessing(root_dir, var_list[0])
    for i in range(1, len(var_list)):
        var_df = pd.merge(var_df, PreProcessing(root_dir, var_list[i]), how='outer')
        
    # (2)-2 열 순서 조정 및 필요없는 'Index' 컬럼 삭제
    var_df = var_df[['Index', 'Date', 'Time', 'Lot', 'pH', 'Temp', 'Voltage']]
    var_df.drop(columns=['Index'], inplace=True)

    return var_df


# (3) csv 파일 하나 단위당 전처리하는 코드
def ErrPreprocessing(root_dir, err_list):
    df = pd.read_csv(os.path.join(root_dir, err_list), engine='pyarrow')
    df.rename(columns = {'0':'Date', '1':'FailureLot1', '2':'FailureLot2'}, inplace=True)
    
    return df

# (4) csv 파일 전부 merge하고 정리하는 코드
def ErrMergeFrame(root_dir, err_list):
    err_df = ErrPreprocessing(root_dir, err_list[0])
    
    # (4)-1 파일이 두 개 이상일 경우에만 merge 작업을 해주면 된다
    if len(err_list) > 1:
        for i in range(1, len(err_list)):
            err_df = pd.merge(err_df, ErrPreprocessing(root_dir, err_list[i]), how='outer')
            err_df = err_df[['Date', 'FailureLot1', 'FailureLot2']]
    else:
        err_df = err_df[['Date', 'FailureLot1', 'FailureLot2']]

    return err_df



'''
3. Airflow 스케줄러 DAG 작성
위의 과정을 스케줄로 할 수 있게 만든다 - 계획: 하루 한 번
'''