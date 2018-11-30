import telebot
import time
#from telebot import apihelper
#import logging

access_token = '793517845:AAFAVxHteiB28UpfxGwEaQRqGOIUlwqIJvM'
# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)

while 1:
    time.sleep(5)
    try:
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            text = "Hello, my name is iKristina"
            bot.send_message(message.chat.id,text )

        @bot.message_handler(commands=['echo'])
        def echo(message):
            bot.send_message(message.chat.id, message.text)

        if __name__ == '__main__':
            bot.polling(none_stop=False, interval=0, timeout=20)
    except:
        time.sleep(5)
        continue