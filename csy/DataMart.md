## 요구사항

- 환경변수 + Error 데이터 하나의 df로 생성 요청
    - Error 컬럼 생성 후 불량 lot는 0, 정상lot는 1로 표시
- Error 데이터에서 lot 정수형태로 변환 요청
- 만들어진 데이터 프레임 MySQL에 저장

## 합쳐진 데이터프레임

![image](https://user-images.githubusercontent.com/108312195/196346037-8ba6d148-30e7-42ae-9088-e452afb6f6e6.png)

- 2021-09-08 error난 20번 Lot가 불량을 뜻하는 0인지 확인

![image](https://user-images.githubusercontent.com/108312195/196346456-7ac9ac16-cc91-424e-bcad-cffecf297210.png)

### CSV로 저장

![image](https://user-images.githubusercontent.com/108312195/196347033-c0b0af64-f2a9-46de-b580-10e8082bbca9.png)

## MySQL에 저장

![image](https://user-images.githubusercontent.com/108312195/196347097-fa36591e-a380-42a7-a202-b371f8eb7140.png)

![image](https://user-images.githubusercontent.com/108312195/196347149-24e41331-6a6d-4d93-8c0b-da3003cc3ec2.png)
