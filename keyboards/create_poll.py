from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, PollType


poll_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
poll_keyboard.add(KeyboardButton("/Создать викторину",
                                        request_poll=KeyboardButtonPollType(type=PollType.QUIZ)))