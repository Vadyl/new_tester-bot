from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, PollType

create = KeyboardButton("/cтворити_тест")
# create = KeyboardButton("/cтворити_тест")

create_button = ReplyKeyboardMarkup()  # resize_keyboard=True
create_button.add(create)


# poll_keyboard.add(KeyboardButton(text="Отмена"))