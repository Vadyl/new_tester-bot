from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , ReplyKeyboardRemove



reg = KeyboardButton("/реєстрація")
log_in = KeyboardButton("/вхід")

start_teacher_buttons = ReplyKeyboardMarkup() # resize_keyboard=True
start_teacher_buttons.add(reg).add(log_in)