import requests
from bs4 import BeautifulSoup
import datetime
import telebot
from telebot import apihelper
import time
from multiprocessing import Process
#from itertools import groupby
import sys
import os
import pytz

sys.setrecursionlimit(5000)

TimeZone=pytz.timezone('Europe/Tiraspol')

token=os.environ.get('BOT_TOKEN')
bot=telebot.TeleBot(token)

#apihelper.proxy = { ' https ' : ' socks5: // @ 176.9.75.42:1080 ' }

URL = 'https://www.agroprombank.com/info/rates.html'
#HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130', 'accept': '*/*'}
HEADERS ={     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
               }

podpiska=["477322157"]
podpiska1=[477322157]

#prod2=float(os.environ.get('prod2'))
#pok2=float(os.environ.get('pok2'))

#file= open(r'prod2.txt','r')
#prod2 = float(file.readline())
#file.close()

#file= open(r'pok2.txt','r')
#pok2 = float(file.readline())
#file.close()

#file1 = open(r'podpiska.txt','r')
#num_lines=len(file1.readlines())
#file1.close()

#file1 = open(r'podpiska.txt','r')
#for y in range(num_lines):
#    podpiska.append((file1.readline()))
#    podpiska1.append(int(podpiska[y]))
#file1.close()

#podpiska[num_lines-1]=(podpiska[num_lines-1]+'\n')

def get_html(url, params=None):
    '''Заходим на сайт'''
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    """"Из всего кода отделяем стоимость и берём 55 и 56 строчку, где находится RUB/RUP"""
    global pok
    global prod
    global pok1
    global prod1
    global prod2
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('td', class_='td')
    pok=(items[55].get_text())
    pok1=float(pok)
    prod=(items[56].get_text())
    prod1=float(prod)

def parse():
    """Проверяем, подключились ли мы к сайту"""
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')

def CURS():
    """Сообщает курс подписчикам"""
    global pok
    global prod
    global pok1
    global prod1
    global prod2
    global d
    global pok2
    print(1)
    while True:
        try:
            parse()
            if (prod2 != prod1) or (pok2 != pok1):
                d = datetime.datetime.now(tz=TimeZone)  # Время на компьютере сейчас
                lengthpok = 6 - len(str(pok2))
                lengthprod = 6 - len(str(prod2))
                bot.send_message(477322157, ('Сейчас ' + d.strftime('%H:%M:%S')))
                if prod1 > prod2:
                    bot.send_message(477322157, ("Курс RUB/RUP повысился:"))
                elif prod1 < prod2:
                    bot.send_message(477322157, ("Курс RUB/RUP понизился:"))
                elif pok1 > pok2:
                    bot.send_message(477322157, ("Курс RUB/RUP повысился:"))
                else:
                    bot.send_message(477322157, ("Курс RUB/RUP понизился:"))
                bot.send_message(477322157, ('Было:   Покупка: ' + str(pok2) + '0' * lengthpok + '      Продажа: ' + str(prod2) + '0' * lengthprod))
                bot.send_message(477322157, ('Стало:  Покупка: ' + pok + '      Продажа: ' + prod))
                time.sleep(1)
                prod2 = prod1
                pok2 = pok1
            time.sleep(60)
        except Exception or ConnectionError or ConnectionResetError or ConnectionAbortedError or RuntimeError or TimeoutError or BaseException as e:
            print(e)
            bot.send_message(477322157, (e))
            time.sleep(5)



bot.send_message(477322157, ("Старт"))
parse()
pok2=pok1
prod2=prod1

CURS()
