# 탐색적 데이터 분석

## description

[공정 환경변수 csv]

column 수 6개, row 수 50,094개, 데이터수 300,564개

| 속성 | 설명 | 비고 |
| --- | --- | --- |
| Index |  데이터 수집 시 자동 생성 값 | int |
| LoT | LoT 추적을 위해, 동일 LoT에 동일 숫자 부여 | int |
| Time | 측정 시 시간을 초 단위까지 기록(H:MM:SS) | timestamps |
| pH | 전처리 설비 내 공정 pH 측정값 | float |
| Temp | 전처리 설비 내 공정 온도 측정값 | float |
| Voltage | 전처리 설비 내 공정 전압 측정값 | float |

![image](https://user-images.githubusercontent.com/108312195/196313676-8270e19e-e6b1-475e-a4ef-1b0e19338d31.png)

[Error Lot list csv]

column 수 3개, row 수 33개, 데이터수 99개

| 속성 | 설명 | 비고 |
| --- | --- | --- |
| 0 | 각 공정이 수행된 날짜 기록(YYYY-MM-DD) | string |
| 1 | LoT 추적을 위해 각 LoT 별로 부여 (Error난 LoT 번호) | int |
| 2 | LoT 추적을 위해 각 LoT 별로 부여 (Error난 LoT 번호) | int |

![image](https://user-images.githubusercontent.com/108312195/196315814-2c1c7cac-6b8e-4408-9601-6cc2a47bd6fc.png)

[정상 이미지 png]

정상 이미지 1,387개, 불량 이미지 74개, 데이터수 1,452개

![image](https://user-images.githubusercontent.com/108312195/196316657-4dd201c3-9880-422c-894b-8854ba780c7c.png)

[불량 이미지 png]

![image](https://user-images.githubusercontent.com/108312195/196316922-ecbf642c-ebcd-43b2-aa22-d4023b2fc385.png)
