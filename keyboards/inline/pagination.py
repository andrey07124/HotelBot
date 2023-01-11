from telegram_bot_pagination import InlineKeyboardPaginator
from loader import bot
from database.db_methods import table_images_output
from loguru import logger
from telebot.types import Message  # эта строчка чисто для if (для разделения веток)


def send_photo_page(message, hotel_db, page=1):
    """
    Функция, создающая клавиатуру пагинации. Выводит пользователю фотографию, соответствующую нажатой кнопке.

    :param message: передает информацию о сообщении.
    :type message: Message.
    :param hotel_db: запись в таблице hotels.
    :type hotel_db: Hotel.
    :param page: передает номер текущей страницы пагинации.
    :type page: int.
    """

    photo_pages = table_images_output(hotel_db)
    hotel_id = str(hotel_db.id)
    string_for_pattern = ''.join([hotel_id, '#photo#{page}'])
    # поместил сюда id отеля чтобы можно было передать его в принимающий хэндлер

    paginator = InlineKeyboardPaginator(
        len(photo_pages),
        current_page=page,
        data_pattern=string_for_pattern
    )

    if isinstance(message, Message) == 1:  # первое сообщение должно отсылаться через send_message
        bot.send_message(
            message.chat.id,
            photo_pages[page-1],
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
    else:
        bot.edit_message_text(photo_pages[page-1], reply_markup=paginator.markup, chat_id=message.message.chat.id,
                              message_id=message.message.message_id, parse_mode='Markdown')
        # чтобы блоки фото с кнопками не перескакивали вниз чата,
        # последующие сообщения отправляю с помощью edit_message_text
