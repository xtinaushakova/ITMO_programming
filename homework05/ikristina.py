import telebot
import time
from schedule_parser import get_page, get_schedule
import re
#from telebot import apihelper
#import logging

access_token = '793517845:AAFAVxHteiB28UpfxGwEaQRqGOIUlwqIJvM'
# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Hello, I'm your friendly schedule bot, at your service! If you get stuck, just type /help to get more info."
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['help'])
def send_help(message):
    text = 'To get your schedule type in your query like this WEEKDAY [GROUP] [WEEK_TYPE]. The default group is K3142, so if you do not specify GROUP I will send you the schedule for that group. If you do not specify WEEK_TYPE I will get you the current week by default. List of commands you can use:\n\n/next\tinfo about next upcoming lesson for today\n/today\t will get you the whole schedule for today\ntomorrow\tprint schedule for tomorrow'
    bot.send_message(message.chat.id,text)


@bot.message_handler(content_types=['text'])
def echo(message):
    text = "Cannot comprehend simple text, can only handle commands. Type /help to get the complete list."
    bot.send_message(message.chat.id, text)

#next
#today
#tomorrow
#all week


if __name__ == '__main__':
    bot.polling(none_stop=True)