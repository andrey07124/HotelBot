from telegram_bot_pagination import InlineKeyboardPaginator
from loader import bot
from database.db_methods import table_images_output
from loguru import logger


def send_photo_page(message, hotel_db, page=1):
    photo_pages = table_images_output(hotel_db)
    hotel_id = str(hotel_db.id)
    logger.debug('hotel_id =', hotel_id)
    string_for_pattern = ''.join([hotel_id, '#photo#{page}'])

    paginator = InlineKeyboardPaginator(
        len(photo_pages),
        current_page=page,
        data_pattern=string_for_pattern
    )

    bot.send_message(
        message.chat.id,
        photo_pages[page-1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
