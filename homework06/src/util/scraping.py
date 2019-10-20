from typing import List
from typing import Tuple
from typing import Dict
from typing import Union

from bs4 import BeautifulSoup

import requests
import time

BASE_URL = 'https://news.ycombinator.com/'


def get_news(url: str = BASE_URL, n_pages: int = 1, crawl_delay: int = 30) -> List[Dict[str, Union[int, str]]]:
    """Возвращает список новостей.

    Parameters
    ----------
    url : str
        Ссылка на страницу с новостями.
    n_pages : int
        Количество страниц, которые нужно обойти.
    crawl_delay: int
        Паузы между GET запросами в секундах.

    Returns
    -------
    list
        Список словарей, описывающих новости.
        Каждый словарь имеет слдующую структуру:
        {'author': 'evo_9',
         'comments': 0,
         'points': 1,
         'title': 'Daily Action – Sign Up to Join the Resistance',
         'url': 'https://dailyaction.org/'}
    """
    batch = []
    news = extract_news(url)
    batch.extend(news)
    n_pages -= 1
    print('Success')

    while n_pages > 0:
        try:
            time.sleep(crawl_delay)
            news, next_page_url = extract_next_page(url)
            url = BASE_URL + next_page_url
            batch.extend(news)
            n_pages -= 1
            print('Success')
        except BaseException:
            print('Failed')

    return batch


def extract_next_page(url: str) -> Tuple[List[Dict[str, Union[int, str]]], str]:
    """Возвращает список новостей на следующей странице и ссылку на эту страницу.

    Parameters
    ----------
    url : str
        Ссылка на страницу с новостями.

    Returns
    -------
    tuple
        Кортеж вида (news: list, next_url: str), где news - список словарей, next_url - строка-ссылка.

    """
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    table = page.table.findAll('table')[1]
    tr = table.find_all('tr').pop()
    next_link = tr.find_all('td')[1].a['href']
    return (extract_news(BASE_URL + next_link), next_link)


def extract_news(url: str) -> List[Dict[str, Union[int, str]]]:
    """Извлекает новости из страницы. Создано сугубо для "https://news.ycombinator.com/".

    Parameters
    ----------
    url : str
        Ссылка на страницу с новостями.

    Returns
    -------
    list
        Список словарей, описывающих новости.
        Каждый словарь имеет слдующую структуру:
        {'author': 'evo_9',
         'comments': 0,
         'points': 1,
         'title': 'Daily Action – Sign Up to Join the Resistance',
         'url': 'https://dailyaction.org/'}

    """
    print(f'Collecting data from page: {url} ...', end=' ')

    news = []

    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    table = page.table.findAll('table')[1]

    # Составим список всех тэгов <tr>, найденных во внутренней таблице.
    trs = table.find_all('tr')

    # Удалим каждый третий <tr>, т.к. он не содержит нужных нам данных.
    del trs[2::3]

    # Удалим два последних <tr> по той же причине.
    trs.pop()
    trs.pop()

    tr = iter(trs)

    for i in range(len(trs)):
        try:
            # Из первого <tr> извлекаем заголовок и ссылку на источник.
            tr1 = next(tr)

            title = tr1.find_all('td')[2].a.text

            # Дополним ссылку слева, если требуется.
            href = tr1.find_all('td')[2].a['href']
            news_url = 'https://news.ycombinator.com/' + href if href.startswith('item?') else href

            # Из второго <tr> извлекаем кол-во лайков и комментов, а также ник автора.
            tr2 = next(tr)

            author = tr2.find_all('td')[1].find_all('a')[0].text

            points_info = tr2.find_all('td')[1].span.text
            points = int(points_info[:len(points_info) - 6])

            comments_info = tr2.find_all('td')[1].find_all('a')[5].text
            if 'discuss' != comments_info:
                comments = int(comments_info[:len(comments_info) - 8])
            else:
                comments = 0

            # Составим запись для новости на основе найденных данных и пополним ей список.
            record = {'author': author,
                      'comments': comments,
                      'points': points,
                      'title': title,
                      'url': news_url}

            news.append(record)

        except StopIteration:
            break

    return news
