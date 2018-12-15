import telebot
import time
from schedule_parser import *
import re
import response

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

@bot.message_handler(commands=['monday', 'MONDAY', 'Monday'])
def monday(message):
	text = get_monday(message)
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['tuesday', 'TUESDAY', 'Tuesday'])
def tuesday(message):
	text = get_tuesday(message)
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['wednesday', 'WEDNESDAY', 'Wednesday'])
def wednesday(message):
	text = get_wednesday(message)
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['thursday', 'THURSDAY', 'Thursday'])
def thursday(message):
	text = get_thursday(message)
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['friday', 'FRIDAY', 'Friday'])
def friday(message):
	text = get_friday(message)
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['saturday', 'SATURDAY', 'Saturday'])
def saturday(message):
	text = get_saturday(message)
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['sunday', 'SUNDAY', 'Sunday'])
def sunday(message):
	text = 'No lessons today. Get some rest, dude and get ready for next week!'
	bot.send_message(message.chat.id, text)

#next
#today
#tomorrow
#all week


@bot.message_handler(content_types=['text'])
def echo(message):
    text = response.simple_text
    bot.send_message(message.chat.id, text)

if __name__ == '__main__':
    bot.polling(none_stop=True)