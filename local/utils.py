import threading
import pandas as pd

def print_menu():
  menu_file = pd.read_csv('./햄버거_메뉴.csv', header=0)
  menu_main = menu_file['햄버거'].dropna()
  menu_side = menu_file['사이드'].dropna()
  menu_drink = menu_file['음료'].dropna()
  # menu_cate = menu_file['category'].dropna()
  # menu_change = menu_file['변경'].dropna()

  printing_line = ["main: ", "side: ", "drink: "]
  menu_list = [menu_main, menu_side, menu_drink]
  for i, menu in enumerate(menu_list):
    print(printing_line[i])
    print('[', end='')
    for i in menu:
      print(i, end='')
      if (i != menu.iloc[-1]) == True:
        print(', ', end='')
    print(']')

  print('\n\n\n')

def get_basket():
  from kiosk_speaker import basket

  print("현재 장바구니: ", end='')
  count = {}
  for m in basket:
    try: count[m] += 1
    except: count[m] = 1
  print(count)

