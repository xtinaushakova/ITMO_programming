import telebot
import time
from schedule_parser import *
import re
import response
import datetime

access_token = '793517845:AAFAVxHteiB28UpfxGwEaQRqGOIUlwqIJvM'
bot = telebot.TeleBot(access_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	text = response.welcome
	bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['help', 'sos', 'HELP', 'Help', 'SOS'])
def send_help(message):
	text = response.help_message
	bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message, group="K3142", week=""):
    a = message.text.split()
    day = a[0]
    if len(a) == 3:
        day, group, week = a
    elif len(a) == 2:
        day, group = a
    web_page = get_page(group, week)
    if day == "/monday":
        day_number = "1"
    elif day == "/tuesday":
        day_number = "2"
    elif day == "/wednesday":
        day_number = "3"
    elif day == "/thursday":
        day_number = "4"
    elif day == "/friday":
        day_number = "5"
    elif day == "/saturday":
        day_number = "6"
    elif day == "/sunday":
        day_number = "7"

    bot.send_message(message.chat.id, get_resp_for_a_day(
        web_page, day_number), parse_mode='HTML')


@bot.message_handler(commands=['near', 'next'])
def get_near_lesson(message, group="K3142", week=""):
    a = message.text.split()
    if len(a) == 3:
        day, group, week = a
    elif len(a) == 2:
        day, group = a
    time = datetime.datetime.now().time()

    day_number = str(datetime.datetime.today().weekday() + 1)

    if time > datetime.time(18, 40, 0):
        para_number = 1
        day_number = str(int(day_number) + 1)
    elif time > datetime.time(17, 00, 0):
        para_number = 7
    elif time > datetime.time(15, 20, 0):
        para_number = 6
    elif time > datetime.time(13, 30, 0):
        para_number = 5
    elif time > datetime.time(11, 40, 0):
        para_number = 4
    elif time > datetime.time(10, 00, 0):
        para_number = 3
    elif time > datetime.time(8, 20, 0):
        para_number = 2


    now_week = datetime.date.today().isocalendar()[1]
    if now_week % 2 == 1:
        week = 2
    else:
        week = 1
    web_page = get_page(group, week)


    while parse_lesson(web_page, day_number, para_number) is None:
        while para_number in range(1,8):
            para_number += 1
        else:
            para_number = 1
            day_number = str(int(day_number) + 1)
            if day_number == '1':
                if week == 2:
                    week = 1
                elif week == 1:
                    week = 2

    bot.send_message(message.chat.id, get_resp_for_a_lesson(
        web_page, day_number, para_number), parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message, group="K3142", week=""):
    a = message.text.split()
    if len(a) == 3:
        day, group, week = a
    elif len(a) == 2:
        day, group = a
    now_week = datetime.date.today().isocalendar()[1]
    if now_week % 2 == 1:
        week = 2
    else:
        week = 1
    web_page = get_page(group, week)

    day_number = str(datetime.datetime.today().weekday() + 2)
    if int(day_number) > 7 and week == 1:
        day_number = '1'
        week = 2
        web_page = get_page(group, week)
    elif int(day_number) > 7 and week == 2:
        day_number = '1'
        week = 1
        web_page = get_page(group, week)

    if parse_schedule_for_a_day(web_page, day_number) is None:
        bot.send_message(message.chat.id, response.no)
    else:
        bot.send_message(message.chat.id, get_resp_for_a_day(
            web_page, day_number), parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message, group="K3142", week=""):
    a = message.text.split()
    if len(a) == 3:
        day, group, week = a
    elif len(a) == 2:
        day, group = a
    mess = ''
    days = {
        '1': 'ПН: ',
        '2': 'ВТ: ',
        '3': 'СР: ',
        '4': 'ЧТ: ',
        '5': 'ПТ: ',
        '6': 'СБ: '
    }
    for i in range(1, 7):
        day_number = str(i)
        if parse_schedule_for_a_day(get_page(group), day_number) is None:
            mess += days[day_number] + 'нет пар' + '\n'
        else:
            mess += days[day_number] + \
                get_resp_for_a_day(get_page(group), day_number) + '\n'

    bot.send_message(message.chat.id, mess, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)