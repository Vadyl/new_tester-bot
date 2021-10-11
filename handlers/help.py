from aiogram import types , Dispatcher

from create_bot import dp , bot



# @dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(process_help_command , commands=['help'])
