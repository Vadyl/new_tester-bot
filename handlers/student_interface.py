from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from create_bot import dp, bot
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, PollAnswer
from create_bot import bot
from create_bot import dp
from keyboards import poll_keyboard, create_button, get_list_of_tests_button
from sql_w import Database

d = Database()

class Reg_student(StatesGroup):
    login = State()
    name = State()
    pin_cod = State()
    name_of_test = State()


def get_tests(login):
    tests_teacher_query = d.user_select_query(
        '''select name from tests join teachers on id_teacher = id_teachers where login = "{0}"'''.format(login))

    tests = []

    for i in tests_teacher_query:
        tests.append(i["name"])

    return tests


# @dp.message_handler(commands=['вчитель'])
async def on_student_click(message: types.Message):
    await Reg_student.login.set()
    text_get_login = "логін вчителя: "

    await bot.send_message(message.from_user.id, text_get_login, reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state = Reg_teacher.name_of_test)
async def get_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
        # print(data['name_of_test'])
    await Reg_student.next()
    await bot.send_message(message.from_user.id, "ім'я учня: ")


# @dp.message_handler(state = Reg_teacher.password)
async def get_name(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['name'] = message.text
    await Reg_student.next()
    await bot.send_message(message.from_user.id, "Пін-код вчителя:")


async def get_pin_cod(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['pin_cod'] = message.text


        await state.finish()

        tests = get_tests(data['login'])


        print(tests)

        tests_button = get_list_of_tests_button(tests)




    await bot.send_message(message.from_user.id, "виберіть тест з наявних: ", reply_markup=tests_button)



    @dp.callback_query_handler(lambda c: c.data)
    async def on_any_test_click(callback_query: types.CallbackQuery):


        id_teacher_query = d.user_select_query('''select id_teacher from teachers where login = "{0}"'''.format(data['login']))[0][
            "id_teacher"]

        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Починаємо тест + {0}'.format(str(callback_query.data)))
        id_tests_query = d.user_select_query(''' select id_test from tests where id_teachers =  '{0}' and name = "{1}"'''.format(id_teacher_query , str(callback_query.data)))[0]["id_test"]
        print(id_tests_query)


        quizzes_query = d.user_select_query(''' select * from quizzes where id_tests = '{0}' '''.format(int(id_tests_query)))



        correct_count = []
        count = []
        print(quizzes_query)

        quizzes = []

        max_count = \
        d.user_select_query(''' select count(*) from quizzes where id_tests = '{0}' '''.format(int(id_tests_query)))[0][
            "count(*)"]

        @dp.callback_query_handler(lambda c: c.data)
        async def push_quiz(callback_query: types.CallbackQuery , i_question):



            options = quizzes_query[i_question]["options"].split(";;;")
            my_quiz = await bot.send_poll(chat_id=message.chat.id, question=quizzes_query[i_question]["question"],
                                is_anonymous=False, options=options, type="quiz",
                                correct_option_id=quizzes_query[i_question]["correct_option_id"])
            quizzes.append(my_quiz)


            print(quizzes_query[i_question]["correct_option_id"])
            print("end")

            print("question", quizzes_query[i_question]["question"])


            @dp.poll_answer_handler()
            async def handle_poll_answer(quiz_answer: PollAnswer):

                i_question = len(count)


                print("!!!!!!!!!!!!!!!!!!!!!!!",  my_quiz.poll.correct_option_id, type(my_quiz.poll.correct_option_id))
                print("!!!!!!!!!!!!!!!!!!!!!!!", quiz_answer.option_ids[0], type(quiz_answer.option_ids[0]))

                print("???????????????" , i_question)
                if quizzes_query[i_question]["correct_option_id"] == quiz_answer.option_ids[0]:
                    await message.reply("правильно")
                    correct_count.append(True)
                else:
                    await message.reply("неправильно")

                count.append(True)

                if len(count) == max_count:
                    await bot.send_message(callback_query.from_user.id, "Дякую що прошли тест.Результат {0}/{1}".format(len(correct_count),max_count))

                    async with  state.proxy() as data:
                        data['name_of_test'] = str(callback_query.data)

                        d.add_data("students" , columns= ("name", "id_tests" ,"count_right_answers") , values=(data["name"],int(id_tests_query),  len(correct_count)) )


                    count.clear()
                    correct_count.clear()
                else:


                    print("bsfikpmokmpokpmokmpokmpokmpokmpokmpokmpokmpokmpokmpo" ,len(count))

                    await push_quiz(callback_query, len(count))

                print(len(correct_count))


        if len(quizzes_query) != 0:
            await push_quiz(callback_query , 0)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(on_student_click, commands=['учень'])
    dp.register_message_handler(get_login, state=Reg_student.login)
    dp.register_message_handler(get_name, state=Reg_student.name)
    dp.register_message_handler(get_pin_cod, state=Reg_student.pin_cod)

