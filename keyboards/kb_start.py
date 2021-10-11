from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , ReplyKeyboardRemove



teacher = KeyboardButton("/вчитель")
student = KeyboardButton("/учень")

start_buttoms = ReplyKeyboardMarkup() # resize_keyboard=True
start_buttoms.add(teacher).add(student)