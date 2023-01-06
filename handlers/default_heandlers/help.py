from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Функция-обработчик команды /help. Посылает в ответ список доступных в боте команд.

    :param message: передает информацию о сообщении.
    :type: Message.
    """

    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))
