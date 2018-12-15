import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import config
import re


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain, 
        week=week, 
        group=group.upper())
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page):
    soup = BeautifulSoup(web_page, "html.parser")
    
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list
	
#parse out week number
#parse out group
#send day 
#the get day 
#send week overview
#next week
#if week specified dont print четная нечетная строка
#получение номера аудитории остается для самостоятельного выполнения

def get_monday(message):
    group = "K3142"
    if re.search(r'\d+\d+\d+\d+', "/monday"):
        _, group = message.text.split()
        group = group.upper()
    web_page = get_page(group)
    print(web_page)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '{}, {}, {}\n'.format(time, location, lesson)
    return resp

def get_tuesday(message):
    group = "K3142"
    if re.search(r'\d+\d+\d+\d+', "/tuesday"):
        _, group = message.text.split()
        group = group.upper()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '{}, {}, {}\n'.format(time, location, lesson)
    return resp

def get_wednesday(message):
    group = "K3142"
    if re.search(r'\d+\d+\d+\d+', "/wednesday"):
        _, group = message.text.split()
        group = group.upper()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '{}, {}, {}\n'.format(time, location, lesson)
    return resp

def get_thursday(message):
    group = "K3142"
    if re.search(r'\d+\d+\d+\d+', "/thursday"):
        _, group = message.text.split()
        group = group.upper()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '{}, {}, {}\n'.format(time, location, lesson)
    return resp

def get_friday(message):
    group = "K3142"
    if re.search(r'\d+\d+\d+\d+', "/friday"):
        _, group = message.text.split()
        group = group.upper()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '{}, {}, {}\n'.format(time, location, lesson)
    return resp

def get_saturday(message):
    group = "K3142"
    if re.search(r'\d+\d+\d+\d+', "/saturday"):
        _, group = message.text.split()
        group = group.upper()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '{}, {}, {}\n'.format(time, location, lesson)
    return resp

#get day
#get week

if __name__ == '__main__':
    week = 0
    group = "K3141"
    print(get_page(group))