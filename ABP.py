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

podpiska=[]
podpiska1=[]

#prod2=float(os.environ.get('prod2'))
#pok2=float(os.environ.get('pok2'))

#file= open(r'prod2.txt','r')
#prod2 = float(file.readline())
#file.close()

#file= open(r'pok2.txt','r')
#pok2 = float(file.readline())
#file.close()

file1 = open(r'podpiska.txt','r')
num_lines=len(file1.readlines())
file1.close()

file1 = open(r'podpiska.txt','r')
for y in range(num_lines):
    podpiska.append((file1.readline()))
    podpiska1.append(int(podpiska[y]))
file1.close()

podpiska[num_lines-1]=(podpiska[num_lines-1]+'\n')


def plus_podp():
    global podpiska
    podpiska=list(set(podpiska))

    #file = open('podpiska.txt', 'w')
    #for x in podpiska:
    #    file.write((str(x)))
    #file.close()

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

@bot.message_handler(content_types=['text'])
def lalala(message):
    """Действия бота, когда ему отправлено сообщение"""
    global podpiska
    global d
    d = datetime.datetime.now(tz=TimeZone) #Время на компьютере сейчас
    parse()
    if message.text.lower() == 'узнать курс':
        bot.send_message(message.chat.id,('Сейчас ' + d.strftime('%H:%M:%S')))
        bot.send_message(message.chat.id,("Курс рубля:"))
        bot.send_message(message.chat.id,('RUB/RUP:  Покупка: '+ pok + '      Продажа: ' + prod),reply_markup=keyboard1)
    elif message.text.lower() == 'добавиться в подписку на курс':
        for x in [podpiska1]:
            if message.chat.id in x:
                bot.send_message(message.chat.id, ("Вы уже подписаны на курс рубля"),reply_markup=keyboard1)
            else:
                podpiska.append(message.chat.id)
                plus_podp()
                bot.send_message(477322157, (d.strftime('%H:%M:%S')))
                bot.send_message(477322157, (message.chat.id))
                bot.send_message(477322157, (message.from_user.username))
                bot.send_message(477322157, (message.from_user.first_name))
                bot.send_message(477322157, (message.from_user.last_name))
                bot.send_message(message.chat.id, ("Вы подписались на курс рубля!"),reply_markup=keyboard1)
    elif message.text.lower() == '/start':
        bot.send_message(message.chat.id, ("Здравствуйте! Я бот🤖, который может присылать вам курс российского рубля!"),reply_markup=keyboard1)
    else: bot.send_message(message.chat.id,("Неизвестная команда"),reply_markup=keyboard1)
    print(d.strftime('%H:%M:%S'))
    print(message.chat.id)
    print(message.from_user.username)
    print(message.from_user.first_name)
    print(message.from_user.last_name )
    print(message.text,'\n')
    #file3 = open('logs.txt.', 'a')
    #file3.writelines(d.strftime('%H:%M:%S')+'\n')
    #file3.writelines(str(message.chat.id)+'\n')
    #file3.writelines(message.from_user.username+'\n')
    #file3.writelines(message.from_user.first_name+'\n')
    #file3.writelines(message.from_user.last_name+'\n' )
    #file3.writelines((message.text+'\n'*2))
    #file3.close()

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Узнать курс', 'Добавиться в подписку на курс')

def CURS():
    """Сообщает курс подписчикам"""
    global pok
    global prod
    global pok1
    global prod1
    global prod2
    global d
    global pok2
    while True:
        print('st')
        d = datetime.datetime.now(tz=TimeZone)  # Время на компьютере сейчас
        parse()
        pok1=0.2222
        prod1=0.2222
        lengthpok=6-len(str(pok2))
        lengthprod=6-len(str(prod2))
        if (prod2!= prod1) or (pok2!=pok1):
            for y in range(len(podpiska)):
                r=podpiska[y]
                bot.send_message(r, ('Сейчас ' + d.strftime('%H:%M:%S')))
                if prod1>prod2:
                    bot.send_message(r, ("Курс RUB/RUP повысился:"))
                elif prod1<prod2:
                    bot.send_message(r,("Курс RUB/RUP понизился:"))
                elif pok1>pok2:
                    bot.send_message(r, ("Курс RUB/RUP повысился:"))
                else:
                    bot.send_message(r, ("Курс RUB/RUP понизился:"))
                bot.send_message(r,('Было:   Покупка: ' + str(pok2)+'0'*lengthpok + '      Продажа: ' + str(prod2)+'0'*lengthprod))
                bot.send_message(r,('Стало:  Покупка: ' + pok + '      Продажа: ' + prod),reply_markup=keyboard1)
            #prod2=prod1
            #pok2=pok1
            #file = open('prod2.txt', 'w')
            #file.writelines(str(prod1))
            #file.close()
            #file = open('pok2.txt', 'w')
            #file.writelines(str(pok1))
            #file.close()
        time.sleep(60)



def start_proc():
    p1=Process(target=CURS, args=())
    p1.start()

    
bot.send_message(477322157,("Старт"))
parse()
#pok2=0
#prod2=0
pok2=pok1
prod2=prod1


if __name__=='__main__':
    start_proc()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception or ConnectionError or ConnectionResetError or ConnectionAbortedError or RuntimeError or TimeoutError or BaseException as e:
            print(e)
            # повторяем через 5 секунд в случае недоступности сервера Telegram
            time.sleep(5)
