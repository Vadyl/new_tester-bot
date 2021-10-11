from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
from create_bot import dp, bot
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from create_bot import dp
# from sql import Database


class Reg_teacher(StatesGroup):
    name_of_test = State()
    password = State()


# @dp.message_handler(commands=['вчитель'])
async def on_teacher_click(message: types.Message):
    await Reg_teacher.name_of_test.set()
    text_get_login = "Давайте створим тест\nНазва теcту:"

    await bot.send_message(message.from_user.id, text_get_login, reply_markup=ReplyKeyboardRemove())



# @dp.message_handler(state = Reg_teacher.name_of_test)
async def get_name_of_test(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['name_of_test'] = message.text
        # print(data['name_of_test'])
    await Reg_teacher.next()
    await bot.send_message(message.from_user.id, "Пароль від тесту:")


# @dp.message_handler(state = Reg_teacher.password)
async def get_password(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['password'] = message.text
        # a = Database
        print(data["name_of_test"], data["password"])

    await state.finish()


def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(on_teacher_click, commands=['вчитель'], state=None)
    dp.register_message_handler(get_name_of_test, state=Reg_teacher.name_of_test)
    dp.register_message_handler(get_password, state=Reg_teacher.password)