from loader import bot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.request_to_api import request_to_api
from config_data import config  # Импорт ключа от API
import json


def city(message: Message) -> None:
    """Функция, отправляющая кнопки с вариантами локаций"""
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup(message))


def city_markup(message: Message) -> InlineKeyboardMarkup:
    """Функция, создающая клавиатуру с кнопками"""
    cities = city_founding(message)
    destinations = InlineKeyboardMarkup()
    for i_city in cities:
        destinations.add(InlineKeyboardButton(text=i_city['city_name'],
                                              callback_data=f'{i_city["destination_id"]}'))
    return destinations


def city_founding(message: Message):
    """Функция, возвращает список словарей с нужным названием города и id
     для дальнейшего использования в кнопках"""

    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": message.text, "locale": "ru_RU"}
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = request_to_api(url, headers, querystring)  # вызов общей функции для запросов
    # Делаю проверку наличия ключа в тексте, а затем подгружаю json.
    if 'sr' in response.text:
        result = json.loads(response.text)  # Десериализация JSON
        sr: dict = result.get('sr', {})  # получаю кусок словаря - список

        cities = list()
        for destination in sr:  # Обрабатываем результат в списке
            if 'gaiaId' in destination:
                cities.append({'city_name': destination['regionNames']['shortName'],
                               'destination_id': destination['gaiaId']
                               }
                              )

    else:
        cities = 'Ошибка, не найдено место назначения.'

    return cities
