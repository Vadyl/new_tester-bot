from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , ReplyKeyboardRemove



create = KeyboardButton("/cтворити_тест")

create_button = ReplyKeyboardMarkup()  # resize_keyboard=True
create_button.add(create)