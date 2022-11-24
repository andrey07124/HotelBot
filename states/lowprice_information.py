from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    city_id = State()  # id города из запроса
    date_in = State()  # Дата заселения
    date_out = State()  # Дата выезда из отеля
    hotels_number = State()  # Количество отелей, которые необходимо вывести в результате (не больше
                            # заранее определённого максимума).
    need_for_photos = State()  # Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
    photos_number = State()  # При положительном ответе пользователь также вводит количество
                            # необходимых фотографий (не больше заранее определённого максимума)
