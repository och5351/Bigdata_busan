1. wait_for_downstream : (True or False)
이전 날짜의 task 인스턴스 중 하나라도 실패한 경우에는 해당 DAG는 실행되지 않고 대기

2. Depends_on_past : (True or False)
이전 날짜의 task 인스턴스 중에서 동일한 task 인스턴스가 실패한 경우 실행되지 않고 대기

이 두가지 옵션을 잘 활용한다면 인스턴스 실행 중지를 통해 잘못된 ETL을 방지하고 에러 추적 및 재처리에 도움을 받을 수 있다

---

[ XCom(Cross Communication) ]
Airflow task는 독립적으로 실행되기 때문에 기본적으로 서로 통신할 수단이 없음.
하지만 작업 흐름을 만들다 보면 이전 작업의 결과, 요소 등을 다음 작업에 전달하는 경우 발생.
이때 XCom을 이용해 메세지를 교환.
=> Task 간의 통신을 위한 메모 정도의 목적으로 설계, 대용량 파일 전송 등의 용도로는 적합하지 않음
=> XCom을 적용하기 위해서는 "provide_context":True 설정이 꼭 있어야 함