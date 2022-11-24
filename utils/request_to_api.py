import requests
from requests.exceptions import HTTPError, Timeout


def request_to_api(url, headers, querystring):
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        # использую timeout у запроса, чтобы не ждать продолжительное время ответа от сервера
        if response.status_code == requests.codes.ok:  # Проверяю статус-код прежде чем десереализовать ответ в объект
            return response
        response.raise_for_status()  # Если запрос не успешный, сработает ошибка HTTP
    except HTTPError as http_err:
        print(f'Ошибка HTTP {http_err}')
    except Timeout as time_err:
        print(f"Время запроса иcтекло {time_err}")
    except ConnectionError as err:  # TODO какие ошибки здесь описывать? И как правильно обработать?
        print(f'Ошибка соединения {err}')
