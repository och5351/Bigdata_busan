1. test가 적힌 것들은 모두 test를 위해 airflow에 넣어둔 코드(학습목적, 삭제X)

2. main으로 사용하는 코드
- main_schedulevar.py : 공정환경변수들을 MySQL에 저장 스케줄링
- main_scheduleerr.py : 에러로트들을 MySQL에 저장 스케줄링
- main_labelmodel.py : MySQL에 저장된 공정환경변수들과 에러로트들을 불러내어 라벨링 작업하고 MySQL에 저장 스케줄링