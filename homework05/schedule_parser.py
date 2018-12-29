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
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, day_number: str):
    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": day_number + "day"})

    if schedule_table is None:
        return None
    else:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text + ", " +
                          room.dd.text for room in locations_list]

        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info])
                        for lesson_info in lessons_list]

        return times_list, locations_list, lessons_list


def parse_lesson(web_page, day_number: str, para_number: int):

    soup = BeautifulSoup(web_page, "html5lib")

    schedule_table = soup.find("table", attrs={"id": day_number + "day"})

    if schedule_table is None:
        return None
    else:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text + ", " +
                          room.dd.text for room in locations_list]

        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info])
                        for lesson_info in lessons_list]

        paras = {1: '08:20-09:50',
                 2: '10:00-11:30',
                 3: '11:40-13:10',
                 4: '13:30-15:00',
                 5: '15:20-16:50',
                 6: '17:00-18:30',
                 7: '18:40-20:10'}

        for i in range(len(times_list)):
            if times_list[i] == paras[para_number]:
                return times_list[i], locations_list[i], lessons_list[i]


def get_resp_for_a_day(web_page, day_number: str):
    times_lst, locations_lst, lessons_lst = parse_schedule_for_a_day(
        web_page, day_number)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}'.format(time, location, lesson)
    return resp


def get_resp_for_a_lesson(web_page, day_number: str, para_number: int):
    time, location, lesson = parse_lesson(web_page, day_number, para_number)
    resp = '<b>{}</b>, {}, {}'.format(time, location, lesson)
    return resp
