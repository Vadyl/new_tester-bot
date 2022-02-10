from aiogram import types , Dispatcher

from create_bot import dp , bot

from keyboards import start_buttoms , create_button

# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):

    try:
        text = "Для початку виберіть під ким хочете залогінитись"


        await bot.send_message(message.from_user.id, text , reply_markup = start_buttoms)
        await message.delete()
    except:
        await message.reply("Помилка! Якщо ви викликали бота в групі , то спробуйте написати боту /start в лс:\n "
                            "https://t.me/All_tester_bot")




def register_handlers_client(dp : Dispatcher):

    dp.register_message_handler(process_start_command, commands=['start'])