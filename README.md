# k.A.I_speaker

## DESCRIPTION

STT와 다중분류모델을 이용한 '음성 인식 AI 서비스'

STT를 이용하여 명령 음성을 텍스트로 변환한 뒤 다중분류 모델을 통해 해당 명령의 카테고리를 분류하고

카테고리에 맞는 동작을 rule_base 이용하여 해당 동작을 수행합니다.





## PROGRAM LANGUAGE

python3




## LIBRARY USED

gluonnlp == 0.10.0

sentencepiece==0.1.91

pandas

transformers==4.8.2

tqdm

torch==1.8.2

mxnet




## FUNCTION

- speech_to_text()
    
    ## DESCRIPTION
    
    음성인식(Speech Recognition)을 위한 **STT**(Speech-to-Text).
    
    음성녹음으로 오디오파일을 생성한 뒤 recognize_gogle 모듈을 이용하여  text로 변환합니다.
    
    ## PARAMETER
    
    (NONE)
    
    ## RETURN
    
    text: str, 명령 음성이 변환된 텍스트
    
- predict(text, model, tok, vocab)
    
    ## DESCRIPTION
    
    다중분류 모델을 이용하여 명령의 카테고리를 분류합니다.
    
    토큰화, 패딩, 임베딩, torch형식으로 변환, 데이터로더로부터 input값 가져오는 과정을 거친 후
    
    argmax를 통해 예측값을 분석합니다.
    
    ## PARAMETER
    
    text: str, 텍스트로 변환된 명령어 
    
    model: 학습된 kobert 기반 다중분류 인공지능 모델
    
    tok: 한국어 tokenizer
    
    vocab: 한국어 tokenizer vocabulary
    
    ## RETURN
    
    category: str, 모델이 분류한 명령의 카테고리 
    
- rule_base(category, text, okt )
    
    ## DESCRIPTION
    
    분류된 카테고리를 이용하여 각 카테고리에 맞는 룰 베이스 함수로 분기하는 함수.
    
    주문, 변경, 결제, 추천, 메뉴판 함수로 분기 시키며 각 함수들의 성공/실패 여부를 확인하여 흐름을 제어합니다.
    
    ## PARAMETER
    
    category: 모델이 분류한 명령의 카테고리 
    
    text: 텍스트로 변환된 명령어 
    
    okt: 한국어 형태소 분석기
    
    ## 구성
    
    | FUNCTION | DESCRIPTION | PARAMETER | RETURN |
    | --- | --- | --- | --- |
    | deal_order(text, okt) | 주문 | text, okt | 0/1(실패/성공) |
    | deal_changing(text, okt) | 변경 | text, okt | 0/1(실패/성공) |
    | deal_pay() | 결제 | (NONE) | 0/1(실패/성공) |
    | deal_recommand() | 추천 | (NONE) | 0/1(실패/성공) |
    | deal_menulist() | 메뉴판 | (NONE) | 0/1(실패/성공) |
    
    ## RETURN
    
    (NONE)
    




## VARIABLE

global basket : 장바구니

global ALARM_FLAG : 결제&변경 알람 프로세스 처리






## 다중분류모델 예측 결과 예시

<img width="452" alt="Screen Shot 2021-11-21 at 12 25 43 AM" src="https://user-images.githubusercontent.com/68856374/143580578-6dedef00-1e7a-41e6-8d4a-3d489c4066cc.png">






## 서비스 이용 예시

<img width="443" alt="Screen Shot 2021-11-26 at 9 22 13 PM" src="https://user-images.githubusercontent.com/68856374/143580709-80421b75-ea92-4739-b368-2a01c2096a03.png">


<img width="447" alt="Screen Shot 2021-1![Uploading Screen Shot 2021-11-26 at 9.22.13 PM.png…]()
1-26 at 9 21 53 PM" src="https://user-images.githubusercontent.com/68856374/143580647-bea32d51-f2b7-473e-98c0-c748b8e50d5b.png">



##### made by hyopark, hson, jijo
