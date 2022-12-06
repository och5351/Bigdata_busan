'''
1. 패키지 import
'''
# 기본 패키지 import
# import pandas as pd
# import numpy as np
# import pyarrow
# from datetime import datetime

# # 디렉토리 관련 패키지
# import os
# import glob
# import natsort

# # MySQL 관련 패키지
# import MySQLdb
# import mysql.connector

# # SQL Alchemy 관련 패키지 1
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.dialects.mysql import *
# from sqlalchemy.types import *

# # SQL Alchemy 관련 패키지 2
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Table, MetaData
# from sqlalchemy import insert, update

# # Airflow 패키지
# import airflow
# import pendulum
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.providers.mysql.operators.mysql import MySqlOperator


from datetime import datetime, timedelta
from textwrap import dedent
import airflow
import pendulum
from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator


'''
2. Airflow DAG 설정 및 선언
'''
# argument 설정
local_tz = pendulum.timezone('Asia/Seoul')
init_args = {
    'owner' : 'airflow'
}

# DAG id 설정하고 argument 반영
init_dag = DAG(
    dag_id = 'test',
    default_args = init_args,
    start_date = datetime(2022, 11, 17, 18, tzinfo=local_tz),
    schedule_interval = '@hourly'
)


'''
3. 테스트 함수
'''
def InputTest():
    # 필요 라이브러리 import
    import pandas as pd
    import numpy as np
    import pyarrow
    import os
    import glob
    import natsort
    import MySQLdb
    import mysql.connector
    import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import Table, MetaData
    from sqlalchemy import insert, update

    # (1) SQL Alchemy로 MySQL에 연결
    url = 'mysql+mysqldb://sixdogma:Poiu0987*@13.113.12.130:3306/Test'
    engine = sqlalchemy.create_engine(url, encoding='utf-8', echo=True)

    # (2) 코드 작성
    engine.execute("INSERT INTO test (col1, col2) VALUES (%s, %s)", ('sixdogma', 'hello'))


'''
4. 오퍼레이터 코드 작성
'''
SQL_Insert = PythonOperator(
    task_id= 'test_sql_insert',
    python_callable = InputTest,
    dag=init_dag
)