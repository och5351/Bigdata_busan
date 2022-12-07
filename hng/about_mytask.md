# 공정환경변수
### 공정환경변수 파일 메인 코드
1. sixdogma_var_input.ipynb

    원천데이터를 MySQL에 저장하는 코드

2. schedule_var > main_schedulevar.py

    공정환경변수 csv 파일들을 airflow를 이용하여 MySQL로 스케줄링 하기 위한 코드

3. schedule_var > main_scheduleerr.py

    에러로트 csv 파일들을 airflow를 이용하여 MySQL로 스케줄링 하기 위한 코드

4. schedule_var > main_labelmodel.py

    MySQL에 저장해둔 공정환경변수 및 에러로트 내역을 불러와서 모델에 필요한 라벨링을 만드는 작업을 airflow를 이용하여 MySQL로 스케줄링 하기 위한 코드

### 공정환경변수 파일 테스트 코드
1. testcode.ipynb

    MySQL 스케줄링을 테스트하기 위해 연습한 코드

2. labeltest.ipynb
    
    airflow 스케줄링 중 오류가 발생하여 임시로 작성한 코드


# 이미지
### 이미지 파일 메인 코드
1. sixdogma_img_input.ipynb

    원천이미지를 blob type으로 변환해서 MySQL에 저장하는 코드

2. schedule_img > main_schedulegood.py

    Flask 웹에 들어오는 이미지 파일들 중 good으로 판정된 이미지들을 airflow를 이용하여 HDFS로 스케줄링 하기 위한 코드

3. schedule_img > main_schedulebad.py

    Flask 웹에 들어오는 이미지 파일들 중 bad로 판정된 이미지들을 airflow를 이용하여 HDFS로 스케줄링 하기 위한 코드
    

### 이미지 파일 테스트 코드
1. schedule_img > hdfscli_test.py

    <a href="https://hdfscli.readthedocs.io/en/latest/api.html">WebHDFS API clients</a>

    WebHDFS API clients를 이용해서 airflow DAG를 테스트해본 코드

2. schedule_img > sftpoperator_test.py

    <a href="https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/connections/sftp.html">SFTP Operator</a>

    airflow의 SFTP Operator를 이용해서 airflow DAG를 테스트해본 코드

3. schedule_img > sshoperator_test.py

    <a href="https://airflow.apache.org/docs/apache-airflow-providers-ssh/stable/connections/ssh.html">SSH Operator</a>

    airflow의 SSH Operator를 이용해서 airflow DAG를 테스트해본 코드

4. schedule_img > webhdfsoperator_test.py

    <a href="https://github.com/mcarujo/twitter-scraper/blob/main/dags/twitter_furiagg_dag.py">WebHDFS Operator</a>

    WebHDFS Operator 예제문을 활용해서 airflow DAG를 테스트해본 코드


# 스터디
1. airflow_study > *

    팀원들끼리 airflow 스터디를 하기 위해 만든 폴더