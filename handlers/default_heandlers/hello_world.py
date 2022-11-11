from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['hello_world'])
def bot_hello_world(message: Message) -> None:
    """Функция-обработчик команды /hello_world. Посылает в ответ сообщение Hello world!

    :param message: передает информацию о сообщении
    :type: Message
    """
    bot.reply_to(message, 'Hello world!')
