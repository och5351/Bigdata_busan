# Attention Is All You Need

- Transformer를 제안한 매우 중요한 논문
- Text 분야를 압도적으로 발전시킴
- BERT 등 최신 Text 모델에서 기본적으로 사용하는 구조
- 이제는 Image 분야에서도 SOTA를 찍고 있다
    - SOTA(State-of-the-art) : 현재 최고 수준의 결과

[참고 깃허브](https://github.com/och5351/Bigdata_busan.git)

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
    
    ![Untitled (1)](https://user-images.githubusercontent.com/108312195/195586550-50c11d85-76b7-4ec6-9969-cab1d0daf110.png)
    
    - 가장 기본적인 형태의 Seq2Seq 모델 동작 원리
    - 단어가 입력될 때마다 hidden state를 갱신 → hidden state로부터 출력값이 end of Sequence가 나올 때까지 반복 → 출력 문장 생성 완료
    - 입력 문장의 길이 길수도, 짧을수도 → 다양한 경우의 수에 대해서 항상 소스 문장의 정보를 고정된 크기로 갖고 있는 것 → 병목현상의 원인
        - 개선 아이디어
            
            ![Untitled (2)](https://user-images.githubusercontent.com/108312195/195586599-f1355620-4f8d-4731-9b9a-d3165f012267.png)
            
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
- Seq2Seq 모델에 **Attention** 메커니즘을 사용
    - 디코더는 **인코더의 모든 출력(outputs)을 참고**한다
    
    ![Untitled (3)](https://user-images.githubusercontent.com/108312195/195586645-6a636456-5ca9-4c80-90ec-3752627efd47.png)
    
    - 출력할 때마다 소스문장에서 나왔던 모든 출력값들을 모두 참고함
    
    [ 세부과정 ]
    
    - 압축된 context vector 하나만 보는 것이 아니라 출력값 전부 고려한 하나의 Weighted sum vector을 구함 → w를 입력으로 같이 넣어줘서 소스 문장에 대한 정보를 모두 고려할 수 있도록 만들어줌 → 성능 향상

### Seq2Seq with Attention: 디코더(Decoder)

- 디코더는 **매번 인코더의 모든 출력 중에서 어떤 정보가 중요한지를 계산**
    - i = 현재의 디코더가 처리 중인 인덱스
    - j = 각각의 인코더 출력 인덱스
        
        ![Untitled (4)](https://user-images.githubusercontent.com/108312195/195586722-bf1467e3-cae8-4fbd-8353-91e9fd7a44f9.png)
        
        [ 에너지 ]
        
        - 디코더 파트에서 이전에 출력했던 정보(Si-1)와 인코더의 모든 출력값(hj)과 비교
        해서 에너지 값 구함
            - 즉, 어떤 h값과 가장 많은 연관성을 가지는지 구할 수 있음
        
        [ 가중치 ]
        
        - 에너지값에 softmax 취해서 상대적인 확률값 구함
        - Ci : 구한 가중치(αij)를 소스문장의 hidden state(hj)에 곱하고 모두 더한 값을 디코더의 입력으로 같이 넣어줌

### Seq2Seq with Attention: 어텐션 시각화

- Attention의 또 다른 장점 : 시각화 가능
- 어텐션 가중치를 사용해 각 출력이 어떤 입력 정보를 참고했는지 알 수 있다
    
    ![Untitled (5)](https://user-images.githubusercontent.com/108312195/195586755-e37e7f50-4c33-4cd0-8e4f-139775e44ce7.png)
    
    - 밝게 표시된 부분이 확률값이 높은 부분
    - 딥러닝이 어떤 요소에 초점을 두고 분류, 생성했는지 알기에 유용하다

### 트랜스포머(Transformer)

- 트랜스포머는 RNN이나 CNN을 전혀 사용하지 않는다
    - 대신 **Positional Encoding**을 사용
        - 단어의 순서 정보를 알려주기 위함
- BERT와 같은 향상된 네트워크에서도 채택됨
- 인코더와 디코더로 구성된다
    - Attention 과정을 여러 레이어에서 반복한다
    
    ![Untitled (6)](https://user-images.githubusercontent.com/108312195/195586889-de7af58f-6db6-4111-bd8a-e4b6be4313b0.png)
    

### 트랜스포머의 동작 원리: 입력 값 임베딩(Embeding)

- 트랜스포머 이전의 **전통적인 임베딩**
    
    ![Untitled (7)](https://user-images.githubusercontent.com/108312195/195586900-f793477f-cebd-4f57-8dca-64216fd5d2ec.png)
    
- RNN을 사용하지 않으려면 위치 정보를 포함하고 있는 임베딩을 사용해야 함
    - 이를 위해 **Positional Encoding** 사용
        
        ![Untitled (8)](https://user-images.githubusercontent.com/108312195/195586930-07bf6c85-fb44-4785-81ac-558f12de866b.png)
        

### 트랜스포머의 동작 원리: 인코더(Encoder)

- 임베딩 끝난 후 **Attention 진행**
    
    ![Untitled (9)](https://user-images.githubusercontent.com/108312195/195586958-e5ad2200-1373-4e4e-a536-c9377fc423c3.png)
    
- 성능 향상을 위해 **잔여 학습(Residual Learning)** 사용
    
    ![Untitled (10)](https://user-images.githubusercontent.com/108312195/195586986-87cb57c3-6b3c-4fb6-a730-18137b053d89.png)
    
    - 특정 레이어를 건너뛰어서 복사된 값을 그대로 넣어주는 기법
    - 기존 정보 입력받으면서, 잔여된 부분만 학습 → 학습 난이도 낮다 → 초기 모델 수렴 속도 빨라짐
        - 다양한 네트워크에서 Residual Learning 함으로써 성능이 좋아지는 것을 목격할 수 있다
- Residual Learning한 후 Normalization까지 수행 한 뒤 결과를 내보냄
- 어텐션(Attention)과 정규화(Normalization) 과정을 반복한다
    - 여러 레이어 중첩
    - **각 레이어는 서로 다른 파라미터**를 가진다
        
        ![Untitled (11)](https://user-images.githubusercontent.com/108312195/195587031-40f2359c-d2e2-40d8-9cfb-6a07eae0f60a.png)
        
    - 입력과 출력의 Dimension은 동일

### 트랜스포머의 동작 원리: 인코더(Encoder)와 디코더(Decoder)

![Untitled (12)](https://user-images.githubusercontent.com/108312195/195587062-d6acf2ae-fcd0-4d69-b460-bb84dd835045.png)

- 인코더의 마지막 레이어의 출력값을 매번 디코더의 레이어에 넣어주는 방식으로 동작
- 하나의 디코더 레이어에선 두개의 Attention사용
    
    [ Self-Attention ]
    
    - 각 단어들이 서로가 서로에게 어떤 가중치를 가지는지 구함
    
    [ Encoder- Decoder Attention]
    
    - 인코더에 대한 정보를 어텐션
    - 출력 되는 단어가 소스문장의 어떤 단어랑 연관이 있는지 구함
    - ex) I am a teacher 에서 번역된 ‘선생님’이란 단어는 I, am, a, teacher 중에서 어떤 단어랑 가장 높은 연관성이 있는지 구한다
- 트랜스포머에서는 **마지막 인코더 레이어의 출력**이 모든 디코더 레이어에 입력된다
    - **n_layers = 4**일 때의 예시
        
        ![Untitled (13)](https://user-images.githubusercontent.com/108312195/195587083-579f65b8-30ae-41be-92bd-e2a3cef522c7.png)
        
        - 일반적으로 인코더, 디코더 레이어 개수는 동일하게 맞춘다
- 트랜스포머에서도 인코더와 디코더의 구조를 따른다
    - 이때 **RNN 사용하지 않고, 인코더와 디코더를 다수 사용**한다는 점이 특징
    - **eos가 나올 때까지** 디코더 여러번 사용
        
        ![Untitled (14)](https://user-images.githubusercontent.com/108312195/195587115-70574cc2-edc9-4e22-8d16-f11c5dcc25fc.png)
        
        - RNN과 다르게 위치 정보를 한꺼번에 넣음 → 한번의 인코더를 거칠때마다 병렬적으로 출력값 구함 → 비교적 계산복잡도 낮게 형성

### 트랜스포머의 동작 원리: 어텐션(Attention)

- 인코더와 디코더는 **Multi-Head Attention 레이어**를 사용한다

*Multi-Head Attention : 각 어텐션은 여러개의 Head를 가짐
- 어텐션을 위한 **세 가지** 입력 요소
    - 쿼리(Query)
        - 물어보는 주체
        - ex) i
    - 키(Key)
        - 물어보는 대상
        - ex) i, am, a, teacher 각 단어
    - 값(Value)
        - Attention score 구한 뒤 value와 곱해서 결과적인 Attention value를 구함
    
    ![Untitled (15)](https://user-images.githubusercontent.com/108312195/195587145-46c569d2-5c57-4010-839e-139f3a5e293c.png)
    
    [ Scaled Dot-Product Attention ]
    
    - 행렬곱 → 스케일링 → 마스크 → 소프트맥스 취해서 비율 구함 → 확률값 * value값 → 가중치 적용된 Attention value 구함
    
    [ Multi-Head-Attention ]
    
    - h개의 서로 다른 value, key, query로 구분됨
        - h개의 서로 다른 Attention 컨셉을 학습 → 더욱 다양한 특징을 학습할 수 있도록 유도해준다는 장점
    - 각 head로부터 나온 Attention값들을 일렬로 Concat → Linear layer(행렬곱) → output
    - 결과적으로 입력, 출력 Dimension 동일하게 나옴
    
    [ Multi-Head-Attention 레이어 수식 ]
    
    ![Untitled (16)](https://user-images.githubusercontent.com/108312195/195587165-69615d5e-d5de-4700-9e90-6109c6e70b81.png)
    *Wo : output Matrix
    

### 트랜스포머의 동작 원리(하나의 단어): Query, Key, Value

- 어텐션을 위해 쿼리, 키, 값이 필요
- 각 단어의 임베딩을 이용해 생성할 수 있다
    
    ![Untitled (17)](https://user-images.githubusercontent.com/108312195/195587201-7f72146c-83dc-43ba-ba21-d49783fca1d2.png)
    
    - 논문에서는 임베딩차원을 512차원이라 언급
    - 지금은 간단히 4차원에 head 2개라 가정
    - (4 x 2) 가중치 matrix가 생성됨
    - 쿼리, 키, 값은 2차원으로 생성됨( ∵ 4/2)

### 트랜스포머의 동작 원리(하나의 단어): Scaled Dot-Product Attention

![Untitled (18)](https://user-images.githubusercontent.com/108312195/195587236-fdb8daa3-eeb4-4b7d-875e-446b0d9af115.png)

[ I love you ]

- i 와 각 key값 행렬곱 수행 →  Attention Energy값 구함 → 정규화를 위해 scaling factor로 나눔 → softmax 취함 → 나온 가중치값에 value 곱해서 모두 더함 → Attention value값 만들어짐

### 트랜스포머의 동작 원리(행렬): Query, Key, Value

- 실제로는 **행렬(matrix) 곱셈 연산**을 이용해 한꺼번에 연산 가능
    
    ![Untitled (19)](https://user-images.githubusercontent.com/108312195/195587268-87cb0809-a07c-4772-b78b-d86ed42ffd43.png)
    
    - I love you 문장, 4차원 → (3 x 4)행렬

### 트랜스포머의 동작 원리(행렬): Scaled Dot-Product Attention

![Untitled (20)](https://user-images.githubusercontent.com/108312195/195587300-7f978029-6b0f-47da-b17b-8a638fc176b3.png)

- 쿼리값을 한꺼번에 각 키값과 곱함 → Attention Energies의 행, 열이 단어의 개수와 동일한 크기를 가짐 → softmax 취함 → 가중치와 value값 곱함 →  Attention value matrix 생성
- **마스크 행렬(mask matrix)을** 이용해 특정 단어는 무시할 수 있도록 한다
    
    ![Untitled (21)](https://user-images.githubusercontent.com/108312195/195587325-6a2e9abb-c751-4d83-b521-d58ae84deeaf.png)
    
    - Attention Energies와 같은 차원의 Mask Matrix를 만듦 → 각 원소 단위로 곱해줌 → 어떠한 단어는 참고하지 않도록 만들어준다 (특정 단어는 Attention하지 않도록 만듦)
    - ex) I에 대해서 love 와 you는 무시하고 싶다면
        - 마스크 값으로 **음수 무한**의 값을 넣어 softmax 함수의 출력이 0%에 가까워지도록 한다

### 트랜스포머의 동작 원리: Multi-Head-Attention

- 어텐션 수행한 n개의 head값들을 일렬로 Concat → 입력 dimension과 같아지게 된다
    
    ![Untitled (22)](https://user-images.githubusercontent.com/108312195/195587349-6563bac0-c41f-483a-aee7-54fb6b3b380f.png)
    
- MultiHead(Q, K, V)를 수행한 뒤에도 **차원(dimension)이 동일하게 유지**된다
    
    ![Untitled (23)](https://user-images.githubusercontent.com/108312195/195587369-61fafdf6-d034-4fae-b716-2863ed140a75.png)
    

### 트랜스포머의 동작 원리: 어텐션(Attention)의 종류

- 트랜스포머에서는 **세 가지 종류의 어텐션(Attention) 레이어**가 사용된다
    - Multi-Head-Attention이 사용되는 위치에 따라 나뉜다
    
    ![Untitled (24)](https://user-images.githubusercontent.com/108312195/195587447-5de10770-eeae-4760-b07f-f23dd5befd5b.png)
    
    [ Encoder Self-Attention ]
    
    - 각 단어가 서로에게 어떠한 연관성을 가지는지 Attention을 통해 구하고, 전체 문장의  representation을 학습함
    
    [Masked Decoder Self-Attention ]
    
    - 출력 단어가 다른 모든 단어를 참고하는 것이 아닌, 앞쪽에 등장한 단어만 참고하도록 함
    - 채팅이 아닌 정상적인 모델이 만들어질 수 있도록 함
        - ex) ‘나는 축구를 했다’에서 ‘축구를’이 ‘했다’를 참고하면 채팅처럼 동작해버림
    
    [ Encoder-Decoder Attention ]
    
    - Query는 디코더에, Key와 Value는 인코더에 있는 상황을 의미
    - 디코더의 Query값이 인코더의 Key, Value값을 참조

### 트랜스포머의 동작 원리: Self-Attention

- Self-Attention은 인코더와 디코더 모두에서 사용된다
    - 매번 **입력 문장에서 각 단어가 다른 어떤 단어와 연관성이 높은 지** 계산할 수 있다
    
    ![Untitled (25)](https://user-images.githubusercontent.com/108312195/195587487-e6522143-422c-49dd-847b-4bcca29529dd.png)
    
    - ‘it’을 출력한다면 ‘it’이 의미하는 단어는 ‘tree’와 ‘it’이 될 것
        - 두 단어에서 더 높은 score를 가지는 방식으로 학습될 확률이 높다

### 트랜스포머의 동작 원리: Positional Encoding

- 위치 정보를 어떤 방식으로 넣을 지에 관함
- **Positional Encoding**은 다음과 같은 주기 함수를 활용한 공식을 사용한다
    - 각 단어의 **상대적인 위치 정보를 네트워크에 입력**한다
    
    ![Untitled (26)](https://user-images.githubusercontent.com/108312195/195587512-bca4f5ab-434d-4f4a-b423-ab9880aa9021.png)
    
    *PE : Positional Encoding의 약자, pos : 각 단어 번호, i : 각 단어에 대한 임베딩 값의 위치
    
- 주기성을 학습할 수 있도록만 하면 어떤 함수든 사용할 수 있다
- sin, cos 처럼 정해진 함수를 사용할 수도 있지만, 위치 임베딩 값을 따로 학습 시켜서 네트워크에 넣을 수 있다
    - 원 논문에서 실제 해본 결과 sin, cos에 비해 성능 차이는 크게 없었다고 말함
- Transformer 이후에 나온 다양한 아키텍처에서는 주기함수가 아닌 학습이 가능한 형태로 별도의 임베딩 레이어를 사용하기도 함

[ 세부 내용 ]

![Untitled (27)](https://user-images.githubusercontent.com/108312195/195587541-98581b59-a92c-4406-98db-169af61c954a.png)

- dmodel 만큼의 임베딩 차원을 가짐(8차원)
- ⭕ (pos, i) → (0, 3)
    - 첫번째 단어의 4번째 임베딩이기 때문이다
- 각 값들이 위의 함수에 들어가서 입력값과 정확히 동일한 dimension을 가지는 위치 인코딩을 만듦 → 각 원소 단위로 더함 → 인코더, 디코더 레이어의 입력값으로 사용됨

- n과 dimension에 대해 각 단어의 위치에 대한 인코딩 정보가 들어가는 방식을 나타내 보았다

    ![Untitled (28)](https://user-images.githubusercontent.com/108312195/195587568-416f2274-6150-490d-8089-147906b4b967.png)