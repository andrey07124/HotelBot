from loader import bot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.request_to_api import request_to_api
from config_data import config  # Импорт ключа от API
import re
import json


def city(message: Message) -> None:
    """Функция, отправляющая кнопки с вариантами локаций"""
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup(message))


def city_markup(message: Message) -> InlineKeyboardMarkup:
    """Функция, создающая кнопки"""
    cities = city_founding(message)
    destinations = InlineKeyboardMarkup()
    for i_city in cities:
        destinations.add(InlineKeyboardButton(text=i_city['city_name'],
                                              callback_data=f'{i_city["destination_id"]}'))
    return destinations


def city_founding(message: Message):
    """Функция, возвращает список словарей с нужным названием города и id
     для дальнейшего использования в кнопках"""

    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": message.text, "locale": "ru_RU", "currency": "USD"}
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = request_to_api(url, headers, querystring)  # вызов общей функции для запросов
    # Делаю проверку наличия ключа в тексте ответа регулярным выражением, а затем подгружаю json.
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        result = json.loads(f"{{{find[0]}}}")  # Десериализация JSON

        cities = list()
        for dest in result['entities']:  # Обрабатываем результат
            clear_destination = re.sub(r'<.+?>', '', dest['caption'])  # убираю лишнее и оставляю только название города
            cities.append({'city_name': clear_destination,
                           'destination_id': dest['destinationId']
                           }
                          )

    else:
        cities = 'Ошибка, не найден CITY_GROUP'

    return cities
