import requests
from requests.exceptions import HTTPError, Timeout
from config_data import config  # Импорт ключа от API
import json
from requests.models import Response  # для аннотации
from typing import Dict, List, Union
from loguru import logger


def pretty(obj: json) -> None:
    """
    Красивое форматирование вывода dict
    :param obj: объект
    :return: None
    """
    json_formatted_str = json.dumps(obj, indent=4, ensure_ascii=False)
    print(json_formatted_str)  # Проверка работы


def request_to_api_post(url: str, headers: Dict[str, str], payload: Dict[str, str]) -> Response:
    """Функция для осуществления get-запросов к API сайта"""
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=14)
        # использую timeout у запроса, чтобы не ждать продолжительное время ответа от сервера
        if response.status_code == requests.codes.ok:  # Проверяю статус-код прежде чем десереализовать ответ в объект
            return response
        response.raise_for_status()  # Если запрос не успешный, сработает ошибка HTTP
    except HTTPError as http_err:
        logger.exception(f'Ошибка HTTP {http_err}')
    except Timeout as time_err:
        logger.exception(f"Время запроса иcтекло {time_err}")
    except ConnectionError as err:
        logger.exception(f'Ошибка соединения {err}')


def hotels_founding(state_data: dict):  # Union[str, List[Dict[Union[str, float]]]]
    # TODO Не могу правильно прописать аннотацию типов
    """Функция, возвращает список словарей с информацией по отелю"""

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": state_data['city_id']},
        "checkInDate": {
            "day": state_data['arrival_date'].day,
            "month": state_data['arrival_date'].month,
            "year": state_data['arrival_date'].year
        },
        "checkOutDate": {
            "day": state_data['departure_date'].day,
            "month": state_data['departure_date'].month,
            "year": state_data['departure_date'].year
        },
        "rooms": [
            {
                "adults": 1,  # Убрал лишнюю строку с детьми
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": state_data['hotels_quantity'],
        "sort": state_data['searching_state'],
        "filters": {
            # "price": {
            #     "max": 150,
            #     "min": 100
            # },  # Только для бестдилл
            "availableFilter": "SHOW_AVAILABLE_ONLY"  # Добавил сам. Чтобы показывало только отели, где есть места
        }
    }
    headers = {
        "content-type": "application/json",  # эту строку можно убрать
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response: Response = request_to_api_post(url, headers, payload)  # вызов общей функции для post-запросов

    hotels = []
    if len(response.text) > 0:
        response: dict = response.json()  # Десериализация JSON.
        data: dict = response.get('data', {})  # Этапы (уровни) смотрел в RapidApi (data->propertySearch->properties)
        property_search: dict = data.get('propertySearch', {})
        # Ошибку нигде не вернет, если что вернет пустые словари и список
        properties: list = property_search.get('properties', [])
        if len(properties) > 0:
            # pretty(properties)  # красивый вывод словаря
            for i_hotel in properties:
                if i_hotel['destinationInfo']['distanceFromDestination']['unit'] == 'MILE':  # расстояние до центра
                    distance_from_destination = i_hotel['destinationInfo']['distanceFromDestination'][
                                                    'value'] * 1.609344
                else:
                    distance_from_destination = i_hotel['destinationInfo']['distanceFromDestination']['value']
                current_hotel = {'name': i_hotel['name'],
                                 'price': i_hotel['price']['lead']['amount'],
                                 'distance_from_destination': distance_from_destination,
                                 'hotel_id': i_hotel['id']}
                current_hotel.update(address_founding(i_hotel['id']))  # вызов функции для парсинга detail
                hotels.append(current_hotel)
    else:
        hotels = 'Отели не найдены'

    return hotels


def address_founding(property_id: str) -> Dict[str, str]:
    """Функция, возвращает список словарей с адресом отеля"""

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": property_id
    }
    headers = {
        "content-type": "application/json",  # эту строку можно убрать
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response: Response = request_to_api_post(url, headers, payload)

    hotels_detail = {}
    response: dict = response.json()  # Десериализация JSON.
    # Этапы (уровни) смотрел в RapidApi (data->propertyInfo->summary->location->address->addressLine)
    data: dict = response.get('data', {})
    # Ошибку нигде не вернет, если что вернет пустые словари
    property_info: dict = data.get('propertyInfo', {})
    summary: dict = property_info.get('summary', {})
    location: dict = summary.get('location', {})
    address: dict = location.get('address', {})
    address_line: str = address.get('addressLine', 'Адрес отеля не найден.')

    hotels_detail['address_line'] = address_line  # адрес

    return hotels_detail


def photo_founding(property_id: str, state_data: dict) -> List[str]:
    """Функция, возвращает список с фотографиями отеля"""

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": property_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response: Response = request_to_api_post(url, headers, payload)

    response: dict = response.json()  # Десериализация JSON.
    # Этапы (уровни) в RapidApi (data->propertyInfo->propertyGallery->images->image->url)
    data: dict = response.get('data', {})
    property_info: dict = data.get('propertyInfo', {})
    property_gallery: dict = property_info.get('propertyGallery', {})
    images: list = property_gallery.get('images', [])
    hotels_photos = []
    if len(images) > 0:
        for i_image in images[:state_data['photo_quantity']]:  # отбираем запрошенное количество фотографий
            image: dict = i_image.get('image', {})
            hotels_photos.append(image['url'])

    else:
        hotels_photos.append('Фотографии отеля не найдены.')

    return hotels_photos


def hotels_founding_bestdeal(state_data: dict):  # Union[str, List[Dict[Union[str, float]]]]
    # TODO Не могу правильно прописать аннотацию типов
    """Функция, возвращает список словарей с информацией по отелю"""

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": state_data['city_id']},
        "checkInDate": {
            "day": state_data['arrival_date'].day,
            "month": state_data['arrival_date'].month,
            "year": state_data['arrival_date'].year
        },
        "checkOutDate": {
            "day": state_data['departure_date'].day,
            "month": state_data['departure_date'].month,
            "year": state_data['departure_date'].year
        },
        "rooms": [
            {
                "adults": 1,  # Убрал лишнюю строку с детьми
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": state_data['hotels_quantity'],
        "sort": state_data['searching_state'],
        "filters": {
            "price": {
                "max": state_data['price_max'],
                "min": state_data['price_min']
            },
            "availableFilter": "SHOW_AVAILABLE_ONLY"  # Добавил сам. Чтобы показывало только отели, где есть места
        }
    }
    headers = {
        "content-type": "application/json",  # эту строку можно убрать
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response: Response = request_to_api_post(url, headers, payload)  # вызов общей функции для post-запросов

    hotels = []
    try:
        if len(response.text) > 0:
            response: dict = response.json()  # Десериализация JSON.
            data: dict = response.get('data', {})  # Этапы (уровни) смотрел в RapidApi (data->propertySearch->properties)
            property_search: dict = data.get('propertySearch', {})
            # Ошибку нигде не вернет, если что вернет пустые словари и список
            properties: list = property_search.get('properties', [])
            if len(properties) > 0:
                # pretty(properties)  # красивый вывод словаря
                for i_hotel in properties:
                    if i_hotel['destinationInfo']['distanceFromDestination']['unit'] == 'MILE':  # расстояние до центра
                        distance_from_destination = i_hotel['destinationInfo']['distanceFromDestination'][
                                                        'value'] * 1.609344
                    else:
                        distance_from_destination = i_hotel['destinationInfo']['distanceFromDestination']['value']
                    if distance_from_destination < state_data['distance']:
                        current_hotel = {'name': i_hotel['name'],
                                         'price': i_hotel['price']['lead']['amount'],
                                         'distance_from_destination': distance_from_destination,
                                         'hotel_id': i_hotel['id']}
                        current_hotel.update(address_founding(i_hotel['id']))  # вызов функции для парсинга detail
                        hotels.append(current_hotel)
                    else:
                        break
        else:
            hotels = 'Отели не найдены'

    except AttributeError as attribute_err:
        hotels = 'По заданным параметрам отелей не найдено. Попробуйте расширить параметры.'
        logger.exception(f'Ошибка AttributeError {attribute_err}')

    return hotels
