from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    city_id = State()  # id города из запроса
    arrival_date = State()  # Дата заселения
    departure_date = State()  # Дата выезда из отеля
    hotels_quantity = State()  # Количество отелей, которые необходимо вывести в результате (не больше
                            # заранее определённого максимума).
    is_photos = State()  # Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
    photo_quantity = State()  # При положительном ответе пользователь также вводит количество
                            # необходимых фотографий (не больше заранее определённого максимума)
    searching_state = State()  # TODO наверно для lowprice/hiprice
    price_min = State()
    price_max = State()
    distance = State()
    the_end = State()  # TODO не пойму для чего это состояние
