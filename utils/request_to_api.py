import requests
from requests.exceptions import HTTPError, Timeout
from requests.models import Response  # для аннотации
from typing import Dict
from loguru import logger


def request_to_api(url: str, headers: Dict[str, str], querystring: Dict[str, str]) -> Response:
    """Функция для осуществления get-запросов к API сайта"""
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=12)
        # использую timeout у запроса, чтобы не ждать продолжительное время ответа от сервера
        if response.status_code == requests.codes.ok:  # Проверяю статус-код прежде чем десереализовать ответ в объект
            return response
        response.raise_for_status()  # Если запрос не успешный, сработает ошибка HTTP
    except HTTPError as http_err:
        logger.exception(f'Ошибка HTTP {http_err}')
    except Timeout as time_err:
        logger.exception(f"Время запроса иcтекло {time_err}")
    except ConnectionError as err:  # TODO какие ошибки здесь описывать? И как правильно обработать?
        logger.exception(f'Ошибка соединения {err}')
