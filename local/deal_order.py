import pandas as pd
import time
from STT import speech_to_text

def rule_base(category, text, okt):

	ret = 0
	if category == '주문':
		ret = deal_order(text, okt)
	elif category == '변경':
		ret = deal_changing(text, okt)
	elif category == '결제' or category == '포인트_적립':
		ret = deal_pay()
	elif category == '추천':
		ret = deal_recommand()
	elif category == '메뉴판':
		ret = deal_menulist()
	else:
		print("주문을 인식하지 못하였습니다. 다시 말씀해주세요.")


	return 0

# deal_menulist
def deal_menulist():
	menu_file = pd.read_csv('./햄버거_메뉴.csv', header=0)
	menu_main = menu_file['햄버거'].dropna()

	cnt = 0
	for menu in menu_file['햄버거']:
		cnt += 1
		if (cnt % 3) == 0:
			print('%10s' % menu)
			print('\n')
			continue
		print('%10s' % menu, '  |  ', end='')
	print('\n')



# deal_orcer
# 각 카테고리에 있는지 확인
# 상세메뉴가 들어온 경우
# 카테고리로 인식되는 경우랑 -> 메뉴판

# 메뉴가 없는 경우(카테고리로도)
# 수량이 안들어왔을 때는 1개라고 인식
# 변경 주문에 대해서는 인식 불가

def deal_order(sentence, okt):
	from kiosk_speaker import basket

	nouns = [noun for noun in okt.phrases(sentence)]
	# print('명사: ', nouns) #테스트용
	nums = [num for num in okt.pos(sentence) if num[1] == 'Number']
	# print('수량: ', nums)

	menu_file = pd.read_csv('./햄버거_메뉴.csv', header=0)
	menu_main = menu_file['햄버거'].dropna()
	menu_side = menu_file['사이드'].dropna()
	menu_drink = menu_file['음료'].dropna()
	menu_cate = menu_file['category'].dropna()

	i = 0
	is_correct_order = 0
	for noun in nouns:
		noun = noun.replace(" ", "")
		if (i < len(nums)):
			quantity = nums[i]
			i += 1
		else:
			quantity = 1

		if menu_main.index[menu_main == noun].to_list(): #메뉴가 있으면
			is_correct_order = 1
			print('메인 메뉴: ', noun, ', 수량: {} 개'.format(quantity))
			basket.append(noun)
		elif menu_side.index[menu_side == noun].to_list():
			is_correct_order = 1
			print('사이드 메뉴: ', noun, ', 수량: {} 개'.format(quantity))
			basket.append(noun)
		elif menu_drink.index[menu_drink == noun].to_list():
			is_correct_order = 1
			print('음료: ', noun, ', 수량: {} 개'.format(quantity))
			basket.append(noun)
		elif menu_cate.index[menu_cate == noun].to_list(): #카테고리로 주문
			is_correct_order = 1
			cnt = 0
			for menu in menu_file[noun].dropna():
				cnt += 1
				if (cnt % 3) == 0:
					print('%10s' % menu)
					print('\n')
					continue
				print('%10s' % menu, '  |  ', end='')
			print('\n')
			break

	if is_correct_order == 0:
		print("주문 메뉴를 인식하지 못했습니다. 다시 말씀해주세요.")

	print("현재 장바구니: ", end='')
	count = {}
	for m in basket:
		try: count[m] += 1
		except: count[m] = 1
	print(count)

	return 0


# deal_changing
# 일단 들어온 주문에 메뉴가 있는지 없는지 확인
#	있으면
# -> 변경재료 있는지 없는지 확인
# 	있으면
#  			 -> 메뉴가 장바구니에 있는지 확인
#  			    있으면 -> 처리
#           없으면 -> 메뉴 장바구니에 담기
# 	없으면 -> 변경하실 재료를 다시 말씀해주세요

# 없으면
# -> 변경하실 메뉴를 말씀해주세요

#  불고기버거에 양상추 추가요 라고 했는데, 장바구니에 불고기버거가 없는 경우
#  불고기버거를 장바구니에 담고, 변경 메뉴판 띄우기

# 추가, 삭제, 수량 변경, 변경(음료, 세트 등), 사이즈 변경

def deal_changing(sentence, okt):
	from kiosk_speaker import basket


	if (basket == []):
		print("주문 내역이 없습니다. 주문 후 변경 해주세요.")
		return(0)

	nouns = [noun for noun in okt.phrases(sentence)]
	nums = [num for num in okt.pos(sentence) if num[1] == 'Number']

	menu_file = pd.read_csv('./햄버거_메뉴.csv', header=0)
	menu_main = menu_file['햄버거'].dropna()
	menu_side = menu_file['사이드'].dropna()
	menu_drink = menu_file['음료'].dropna()
	menu_change = menu_file['변경'].dropna()

	menu = 0
	ingred = 0

	is_in_menu = 0
	for noun in nouns:
		noun = noun.replace(" ", "")
		# 들어온 주문에서 메뉴 인식
		if (menu_main.index[menu_main == noun].to_list() or
			menu_side.index[menu_side == noun].to_list() or
			menu_drink.index[menu_drink == noun].to_list()):
			is_in_menu = 1
			menu = noun

	# 메뉴 있음
	if is_in_menu != 0:
		ingred = 0
		for noun in nouns:
			if menu_change.index[menu_change == noun.replace(" ", "")].to_list():
				ingred = noun
		change = 0
		for noun in nouns:
			if (noun == '추가'):
				change = '추가'
			elif (noun == '변경'):
				change = '변경'
			elif (noun == '삭제'):
				change = '삭제'
			elif (noun == '사이즈'):
				change = '사이즈'
		if (change == 0):
			change = '변경'

		# 재료 없음
		if (ingred == 0):
			print("변경 메뉴: {}".format(menu))
			print("변경하실 재료를 말씀해주세요.")
			print('[', end='')
			for c in menu_change:
				print(c, end='')
				if (c != menu_change.iloc[-1]) == True:
					print(', ', end='')
			print(']')
		else: # 메뉴, 재료 둘 다 있음
			is_in_basket = 0
			for m in basket:
				if menu == m:
					is_in_basket = 1 # 장바구니에 있음
			# 메뉴가 장바구니에 있음
			if is_in_basket == 1:
				print('변경 종류: {0}, 메뉴: {1}, 변경 재료: {2}'.format(change, menu, ingred))
			else: # 메뉴가 장바구니에 없음
				basket.append(menu)
				print('\'{}\' 메뉴를 장바구니에 담았습니다.'.format(menu))
				print("변경하실 재료를 말씀해주세요.")
				print('[', end='')
				for c in menu_change:
					print(c, end='')
					if (c != menu_change.iloc[-1]) == True:
						print(', ', end='')
				print(']')
	else: # 메뉴 없음
		print("변경하실 메뉴를 다시 말씀해주세요.")
		print("현재 장바구니: ", end='')
		count = {}
		for m in basket:
			try: count[m] += 1
			except: count[m] = 1
		print(count)

	return 0


# deal_pay
# 가장 먼저 장바구니 확인
# 멤버십을 말하더라도 주문 확인부터

def deal_pay():
	from kiosk_speaker import basket, is_processing, ALARM_FLAG, print_alarm

	if (basket == []):
		print("주문 내역이 없습니다. 주문 후 결제 해주세요.")
		return(0)
	print("주문하신 메뉴가 맞습니까?")
	print('[주문하신 메뉴]')
	count = {}
	for m in basket:
		try: count[m] += 1
		except: count[m] = 1
	print(count)
	print('\n')

	customer_ans = speech_to_text()
	# customer_ans = input("고객 응답: ")
	if customer_ans == '네' or customer_ans == '맞아요' or customer_ans == '응':
		ALARM_FLAG = 0
		print_alarm()

		print("포인트를 적립하시겠습니까?")
		customer_ans2 = speech_to_text()
		# customer_ans2 = input("고객 응답: ")
		if (customer_ans2 == '네' or customer_ans2 == '할게요'
					or customer_ans2 == '할게' or customer_ans2 == '응'):
			print("적립 번호를 말씀해주세요.")
			customer_ans3 = speech_to_text()
			# customer_ans3 = input("고객 응답: ")
			print('\'{}\' 번호로 포인트가 적립되었습니다.'.format(customer_ans3))

		print("카드를 삽입해주세요.")
		time.sleep(3)
		print("결제가 완료되었습니다.\n3초 뒤에 초기 화면으로 돌아갑니다.")

		is_processing = 0
		basket = []

		for i in range(3,0,-1):
			print(i)
			time.sleep(1)

	else:
		print("주문을 다시 확인해주세요.")


	return 0

# del_recommand
def deal_recommand():
	menu_file = pd.read_csv('./햄버거_메뉴.csv', header=0)
	recommand = menu_file['recommand'].dropna()
	print("저희 매장의 추천 메뉴입니다.")
	print("[", end='')
	for i in recommand:
		print(i, end='')
		if (i != recommand.iloc[-1]) == True:
			print(', ', end='')
	print("]")

	return 0
