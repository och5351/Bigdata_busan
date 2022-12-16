1. test가 적힌 것들은 모두 test를 위해 airflow에 넣어둔 코드(학습 목적, 삭제X)

2. main으로 사용하는 코드
- main_schedulegood_sh.py : good으로 판정된 이미지들을 HDFS의 /imgs/good에 저장 스케줄링
- main_schedulebad_sh.py : bad로 판정된 이미지들을 HDFS의 /imgs/bad에 저장 스케줄링