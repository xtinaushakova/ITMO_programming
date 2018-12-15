import requests
import time
from config import config
from requests import exceptions
from typing import *

JSON = Dict[Any, Any]
Response = JSON
Messages = List

def get(query: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> Optional[Response]:
    """ Выполнить GET-запрос
    :param query: тело GET запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for n in range(max_retries):
        try:
            response = requests.get(query, params=params, timeout=timeout)
            content_type = response.headers.get('Content-Type')
            if not content_type == "application/json; charset=utf-8":
                raise
            return response
        except requests.exceptions.RequestException:
            if n == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** n)
            time.sleep(backoff_value)


def get_friends(user_id: int, fields='') -> Response:
    """ Returns a list of user IDs or detailed\
    information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'access_token': config.get("VK_ACCESS_TOKEN"),
        'user_id': config.get("VK_ID"),
        'fields': fields,
        'v': config.get('VERSION')
    }
    url = "{}/friends.get".format(config.get("DOMAIN"))
    response = get(url, params=query_params)
    return response.json()


def get_message_history(user_id: int, offset=0, count=200) -> Messages:

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    query_params = {
        'domain': config.get("DOMAIN"),
        'access_token': config.get("VK_ACCESS_TOKEN"),
        'user_id': config.get('VK_ID'),
        'offset': offset,
        'count': count,
        'version': config.get("VERSION")
    }
    messages = []
    i = 0
    while i < count:
        if (i / 200) % 3 == 0 and i:
            time.sleep(1)
        if count - i <= 200:
            query_params['count'] = count - i
        url = "{domain}/messages.getHistory?offset={offset}&count={count}&user_id={user_id}&" \
              "access_token={access_token}&v={version}".format(**query_params)
        response = requests.get(url)
        json_doc = response.json()
        fail = json_doc.get('error')
        if fail:
            raise Exception(json_doc['error']['error_msg'])
        messages.extend(json_doc['response']['items'])
        i += 200
        query_params['offset'] += i
    return messages