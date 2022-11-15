from loader import bot
from states.lowprice_information import UserInfoState  # Импортирую состояния
from telebot.types import Message
import requests


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    """Функция-хэндлер. Сначала присваивает пользователю состояние, после того как он ввел эту команду"""
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.full_name}.'
                                           f' Укажите город для поиска отелей.')


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    """Функция-хэндлер. Ловит состояние которое ранее присвоено пользователю и сохраняет его"""
    city_response = requests.get('https://hotels4.p.rapidapi.com/v2/get-meta-data')
    bot.send_message(message.from_user.id, city_response)  # TODO дописать
    bot.set_state(message.from_user.id, UserInfoState.dates, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:  # сохраняем полученные данные в словарь
        data['city'] = message.text
