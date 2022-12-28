from loader import bot
from telebot.types import Message
from loguru import logger
from database.db_methods import table_users_output

logger.add("debug.log", backtrace=True, diagnose=True, level='DEBUG', retention='1 day')


@logger.catch
@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """Функция-хэндлер. Ловит команду history и выводит историю запросов"""

    for i_user in table_users_output(message.chat.id):
        bot.send_message(
            message.from_user.id,
            f'Введенная команда: {i_user.command}.\n'
            f'Дата и время ввода команды: {i_user.timestamp.strftime("%m/%d/%Y, %H:%M:%S")}.'
        )

        for i_hotel in i_user.hotels:
            bot.send_message(message.from_user.id, f'Название отеля: {i_hotel.hotel}\n'
                                                   f'адрес отеля: {i_hotel.address}.')

            for i_image in i_hotel.images:
                bot.send_message(message.from_user.id, f'{i_image.image}.')
