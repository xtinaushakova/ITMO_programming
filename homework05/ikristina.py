import telebot
#import traceback
import time
#from telebot import apihelper
#import logging

access_token = '793517845:AAFAVxHteiB28UpfxGwEaQRqGOIUlwqIJvM'
# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)

# Logger
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

# Configuration
#TG_PROXY = 'https://103.241.156.250:8080'
# Set proxy
#apihelper.proxy = {'http': TG_PROXY}

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':    
    while True:
	    try:
	        bot.polling(none_stop=True)
	    except Exception as e:
	        logger.error(e)
	        time.sleep(15)