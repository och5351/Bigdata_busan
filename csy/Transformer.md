# Attention Is All You Need

- Transformer를 제안한 매우 중요한 논문
- Text 분야를 압도적으로 발전시킴
- BERT 등 최신 Text 모델에서 기본적으로 사용하는 구조
- 이제는 Image 분야에서도 SOTA를 찍고 있다
    - SOTA(State-of-the-art) : 현재 최고 수준의 결과

## 1. Transformer 구조

- 기존의 Sequence Transduction(변환) 모델 : 인코더(Encoder)와 디코더(Decoder)를 포함하는 구조를 바탕으로,

       순환 신경망(Recurrent)나 Convolutional Layer를 사용함
- recurrence와 convolution을 완전히 제거하고 오로지 Attention 메커니즘만을 사용하는 "Transformer"라는 새로운 구조를 제안
