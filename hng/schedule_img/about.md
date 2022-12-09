1. plugins 폴더 안에 있는 파일들은 airflow server의 /airflow/plugins에 넣어줄 것들

2. 나머지 py 파일들은 airflow server의 /airflow/dags에 넣어줄 것들

    -> DAG 구분을 할 수 있도록 dag id 설정

3. test가 적힌 것들은 모두 test를 위해 airflow에 넣어둔 코드(학습 목적, 삭제X)

4. main으로 사용하는 코드
- main_schedulegood_sh.py : good으로 판정된 이미지들을 HDFS의 /imgs/good에 저장 스케줄링
- main_schedulebad_sh.py : bad로 판정된 이미지들을 HDFS의 /imgs/bad에 저장 스케줄링