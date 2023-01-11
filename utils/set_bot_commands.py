from telebot import TeleBot  # для документации
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """
    Выводит список доступных в боте команд с описанием.

    :param bot: созданные в модуле loader.py бот
    :type bot: TeleBot.
    """

    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
