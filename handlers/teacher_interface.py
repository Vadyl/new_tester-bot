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
from keyboards import poll_keyboard , create_button
from quizzer import Quiz

from sql_w import Database


class Reg_teacher(StatesGroup):
    name_of_test = State()
    password = State()

quizzes_database = {}  # здесь хранится информация о викторинах
quizzes_owners = {}  # здесь хранятся пары "id викторины <—> id её создателя"
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
        a = Database()
        print(data["name_of_test"] ,data["password"] )
        v = (data["name_of_test"], data["password"])
        a.add_data("main" ,values=v )
        print(data["name_of_test"], data["password"])
        text = "давайте створимо тест"
        await state.finish()
        await bot.send_message(message.from_user.id, "text", reply_markup=create_button)


 # @dp.message_handler(commands=['cтворити_тест'])
async def on_create_click(message: types.Message):
    # await bot.send_message(message.from_user.id, "прикріпіть вікторину", reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(message.from_user.id, "text", reply_markup=poll_keyboard)
    await message.answer("Нажмите на кнопку ниже и создайте викторину!", reply_markup=poll_keyboard)


async def on_create_poll_click(message: types.Message):
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []

        # Если юзер решил вручную отправить не викторину, а опрос, откажем ему.
    if message.poll.type != "quiz":
        await message.reply("Извините, я принимаю только викторины (quiz)!")
        return

        # Сохраняем себе викторину в память
    quizzes_database[str(message.from_user.id)].append(Quiz(
        quiz_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=message.from_user.id)
    )
    # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
    quizzes_owners[message.poll.id] = str(message.from_user.id)
    print("quizzes_database" , quizzes_database)

    await message.reply(
        f"Викторина сохранена. Общее число сохранённых викторин: {len(quizzes_database[str(message.from_user.id)])}")






def register_handlers_teacher(dp: Dispatcher):

    dp.register_message_handler(on_teacher_click, commands=['вчитель'], state=None)
    dp.register_message_handler(get_name_of_test, state=Reg_teacher.name_of_test)
    dp.register_message_handler(get_password, state=Reg_teacher.password)
    dp.register_message_handler(on_create_click, commands=['cтворити_тест'])
    dp.register_message_handler(on_create_poll_click , content_types=["poll"])