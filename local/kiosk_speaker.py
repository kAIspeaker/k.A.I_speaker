# # Speech Recognition - pyaudio, wave
# !brew install portaudio
# !pip install pyaudio
# !pip install wave

# # STT
# !pip install SpeechRecognition

# # TTS
# !pip install gtts

# # 다중 분류 모델
# !pip install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'
# !pip install mxnet
# !pip install gluonnlp pandas tqdm
# !pip install sentencepiece==0.1.91
# !pip install transformers==4.8.2

# # voice recording on Google Colab
# !pip install ffmpeg-python
# !pip install pydub

# # 일정 시간마다 Time check
# !pip install threading


import time
import threading

from konlpy.tag import Okt

from deal_order import rule_base, deal_changing, deal_pay
from STT import speech_to_text
from utils import get_basket, print_menu

global basket
basket = []
global is_processing
is_processing = 0
global ALARM_FLAG
ALARM_FLAG = 0


def print_alarm():
  global ALARM_FLAG
  global timer

  print("\n결제를 원하시면 \'결제\', 변경을 원하시면 \'변경\'이라고 말씀해주세요.\n")

  timer = threading.Timer(20, print_alarm)
  if ALARM_FLAG == 0:
    timer.cancel()
    return
  timer.start()



def main(model, tok, vocab):
  global basket
  global is_processing
  global ALARM_FLAG

  okt = Okt()

  while True:
    is_processing = 0
    basket = []

    print("주문을 원하시면, '주문' 이라고 말씀해 주세요.\n시각장애인이시면 소지하신 이어폰을 왼쪽 하단에 꽂아주세요.")
    # start = speech_to_text()
    start = input("start: ")
    print('\n')

    if (start.replace(" ", "") == '주문'):
      is_processing = 1
      ALARM_FLAG = 0

      while is_processing == 1:
        if basket != [] and ALARM_FLAG == 0: #결제&변경 알림 처리
          ALARM_FLAG = 1
          print_alarm()

        print("주문을 말씀해주세요.")
        # sentence = speech_to_text()
        sentence = input("주문: ")

        if (sentence == '종료'):
          print("키오스크 주문이 종료되었습니다.\n")
          break
        elif (sentence == '장바구니'):
          get_basket()
        elif (sentence == '변경'):
          ret = deal_changing(sentence, okt)
        elif (sentence == '결제'):
          ret = deal_pay()
        else:
        #   category = predict(sentence, model, tok, vocab)
          # print("카테고리: {}".format(category))
          category = input("카테고리: ")

          rule_base(category, sentence, okt)

        print('\n\n\n')

      ALARM_FLAG = 0
      print_alarm() #결제 완료 및 주문 종료시 결제&변경 알림도 종료

    elif (start == '종료'):
      print("키오스크 주문이 종료되었습니다.")
      break



if __name__ == "__main__":
	print_menu()

	# model, tok, vocab = get_model()

	# main(model, tok, vocab)
	main(0, 0, 0)


