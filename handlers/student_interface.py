from aiogram import types , Dispatcher
from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , ReplyKeyboardRemove
from create_bot import dp , bot

# @dp.message_handler(commands=['учень'])
async def on_student_click(message: types.Message):
    text = "Напиши мне что-нибудь, и я отhbdfgdngnпрпавлю этот текст тебе в ответ!"

    await bot.send_message(message.from_user.id, text, reply_markup=ReplyKeyboardRemove())


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(on_student_click , commands=['учень'])