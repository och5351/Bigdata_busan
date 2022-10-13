# Attention Is All You Need

- Transformer를 제안한 매우 중요한 논문
- Text 분야를 압도적으로 발전시킴
- BERT 등 최신 Text 모델에서 기본적으로 사용하는 구조
- 이제는 Image 분야에서도 SOTA를 찍고 있다
    - SOTA(State-of-the-art) : 현재 최고 수준의 결과

# 논문 내용 정리

> 현대의 자연어 처리 딥러닝 모델에 중대한 영향을 끼친 논문인 Transformer(NIPS 2017)를 소개합니다. 2020년을 기준으로 15,000번의 인용 횟수를 가진 Transformer 논문은 매우 많은 최신 자연어 처리 모델이 활용하고 있는 아키텍처를 제안합니다. 이러한 Transformer의 메인 아이디어는 BERT, GPT와 같은 최신 아키텍처에서도 채택되어 세계적으로 유명한 번역 프로그램인 Google 번역기, 네이버 파파고 등에서도 활용되고 있습니다.
*아키텍처 : 시스템 구성 및 동작 원리
> 

## Attention 매커니즘을 전적으로 사용하는 아키텍처

### 딥러닝 기반의 기계 번역 발전 과정

- 자연어 처리에서 가장 중요한 task → 기계 번역
- 2021 기준 최신 고성능 모델들은 Transformer 아키텍처 기반
    - GPT : Transformer의 Decoder 아키텍처 활용
    - BERT : Transformer의 Encoder 아키텍처 활용
    
![Untitled](https://user-images.githubusercontent.com/108312195/195584701-9c863690-62a0-41ae-8ff5-bfa345e7155e.png)

[ LSTM ]

- 다양한 시퀀스 정보 모델링
- 주가 예측, 주기 함수 예측

[ Seq2Seq ]

- 이때까지만 해도 소스 문장을 고정된 크기의 한 vector에 압축해야 함 → 성능적 한계
- 여기에 Attention 기법을 적용해 성능을 끌어올림

[ Transformer ]

- 등장 이후 더이상 RNN 기반 아키텍처를 잘 이용하지 않고 Attention 메커니즘 많이 사용
    *메커니즘 : 사물의 작용 원리나 구조
- Attention 등장 이후 연구 방향이 입력 시퀀스 전체에서 정보를 추출하는 방향으로 발전했다

### 기존 Seq2Seq 모델들의 한계점

- context vector v에 소스 문장의 정보를 압축해야 한다는 점
    
    *context vector : 문맥 벡터
    
    - 병목현상이 발생 → 성능 하락의 원인이 됨
- 한쪽의 Seq로부터 다른 한쪽의 Seq를 만든다는 의미에서 Seq2Seq라 함
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0c753d47-1e2e-43e3-9540-5335bf028890/Untitled.png)
    
    - 가장 기본적인 형태의 Seq2Seq 모델 동작 원리
    - 단어가 입력될 때마다 hidden state를 갱신 → hidden state로부터 출력값이 end of Sequence가 나올 때까지 반복 → 출력 문장 생성 완료
    - 입력 문장의 길이 길수도, 짧을수도 → 다양한 경우의 수에 대해서 항상 소스 문장의 정보를 고정된 크기로 갖고 있는 것 → 병목현상의 원인
        - 개선 아이디어
            
            ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ecfb7077-497f-4d48-815f-98efef947f1d/Untitled.png)
            
            - Decoder가 context vector를 매번 참고할 수도 있다
                - context vector에 대한 정보가 RNN셀을 거침에 따라서 정보가 손실 되는 정도를 줄일 수 있다
                - 출력되는 문장이 길어져도 각 출력되는 단어에 context vector 정보를 다시 넣어줄 수 있어서 성능이 조금 개선된다
            - 다만 여전히 소스 문장을 하나의 벡터에 압축해야 한다는 점은 동일 → 병목현상 여전

### Seq2Seq with Attention

 [ 문제 상황 ]

- 하나의 문맥 벡터가 소스 문장의 모든 정보를 가지고 있어야 하므로 성능이 저하된다

[ 해결 방안 ]

- 매번 소스 문장에서의 출력 전부를 입력으로 받으면?
    - 최신 GPU는 많은 메모리와 빠른 병렬 처리를 지원
