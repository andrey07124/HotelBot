from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Функция-хэндлер, которая ловит текстовые сообщения без указанного состояния. Отправляет сообщение-эхо.

    :param message: передает информацию о сообщении.
    :type: Message.
    """

    bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение: "
                          f"{message.text}")
