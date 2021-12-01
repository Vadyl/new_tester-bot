from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, PollAnswer
from create_bot import bot
from create_bot import dp
from keyboards import poll_keyboard, create_button , start_teacher_buttons
from sql_w import Database


class Reg_teacher(StatesGroup):
    login = State()
    password = State()
    pin_cod = State()

class Enter_teacher(StatesGroup):
    login = State()
    password = State()

class Reg_name_of_test(StatesGroup):
    name_of_test = State()


quizzes_database = {}  # здесь хранится информация о викторинах
quizzes_owners = {}  # здесь хранятся пары "id викторины <—> id её создателя"


# @dp.message_handler(commands=['вчитель'])
async def on_teacher_click(message: types.Message):

    # await Enter_teacher.login.set()
    text = "Ви новий чи ні"


    await bot.send_message(message.from_user.id, text, reply_markup=start_teacher_buttons)


    # await bot.send_message(message.from_user.id, text, reply_markup=start_teacher_buttons)

# @dp.message_handler(state = Reg_teacher.name_of_test)

async def on_enter_click(message: types.Message):
    await Enter_teacher.login.set()

    text_get_login = "Ваш логін:"
    await bot.send_message(message.from_user.id, text_get_login, reply_markup=ReplyKeyboardRemove())


async def get_enter_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
        # print(data['name_of_test'])
    await Enter_teacher.next()
    await bot.send_message(message.from_user.id, "Пароль від аккаунту:")

async def get_enter_password(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['password'] = message.text
        a = Database()

        id_teacher_query = a.user_select_query( '''select * from teachers where login = '{0}' and password = '{1}' '''.format(data['login'],data['password']))

        if len(id_teacher_query) == 0:
            await bot.send_message(message.from_user.id, "Немає користувача з таким логіном і паролем")
        else:
            await bot.send_message(message.from_user.id, "Вітаю " + id_teacher_query[0]['login'])

        id_test_query = a.user_select_query('''select tests.name, students.name, students.count_right_answers 
                                            from tests
                                            join students on id_tests = id_test
                                            where id_teachers = {0} '''.format(id_teacher_query[0]['id_teacher']))

        for i in range(len(id_test_query)):
            current_row = id_test_query[i]
            # select
            # count(*) as count
            # from quizzes
            # where
            # id_tests = 14

            info_text = "Назва тесту: {0}\n Ім'я тесту: {1}\nРезультат {2}".format(current_row["name"],current_row["students.name"], current_row["count_right_answers"])

            await bot.send_message(message.from_user.id,info_text )


        # print(id_teacher_query[0]['password'])
        # print(len(id_teacher_query))



    await bot.send_message(message.from_user.id, " ibv ", reply_markup=create_button)

    await state.finish()



async def on_register_click(message: types.Message):
    await Reg_teacher.login.set()

    text_get_login = "Зареєструйтесь будь ласка \nВаш логін:"
    await bot.send_message(message.from_user.id, text_get_login, reply_markup=ReplyKeyboardRemove())


async def get_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
        # print(data['name_of_test'])
    await Reg_teacher.next()
    await bot.send_message(message.from_user.id, "Пароль від аккаунту:")


# @dp.message_handler(state = Reg_teacher.password)
async def get_password(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['password'] = message.text
    await Reg_teacher.next()
    await bot.send_message(message.from_user.id, "Пін-код від аккаунту:")

async def get_pin_cod(message: types.Message, state: FSMContext):
    async with  state.proxy() as data:
        data['pin_cod'] = message.text

    print(data['login'], data['password'], data['pin_cod'])
    a = Database()
    a.add_data("teachers", columns=["id_teacher", "login", "password", "pin_cod"], values= (message.from_user.id, data['login'] , data['password'], data['pin_cod']))
    await state.finish()
    await bot.send_message(message.from_user.id, "text", reply_markup=create_button)


        #
        # text = "давайте створимо тест"
        # await state.finish()
        # await bot.send_message(message.from_user.id, "text", reply_markup=create_button)


# @dp.message_handler(commands=['cтворити_тест'])
async def on_create_click(message: types.Message):
    # await bot.send_message(message.from_user.id, "прикріпіть вікторину", reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(message.from_user.id, "text", reply_markup=poll_keyboard)
    await Reg_name_of_test.name_of_test.set()
    text_get_name = "Назва тесту: "

    await bot.send_message(message.from_user.id, text_get_name, reply_markup=ReplyKeyboardRemove())
async def on_save_test(message: types.Message):
    #await Enter_teacher.login.set()

    text_get_login = "Тест збережено:"
    await bot.send_message(message.from_user.id, text_get_login, reply_markup=ReplyKeyboardRemove())

    # await Reg_teacher.login.set()
    # text_get_login = "Зареєструйтесь будь ласка \nВаш логін:"
    #
    # await bot.send_message(message.from_user.id, text_get_login, reply_markup=ReplyKeyboardRemove())


async def get_name_of_test(message: types.Message, state: FSMContext):
    print("hello")
    async with  state.proxy() as data:
        data['name_of_test'] = message.text
        global name_test
        name_test = data['name_of_test']


    print(data['name_of_test'])
    a = Database()
    a.add_data("tests", columns=[ "name" , "id_teachers"],
               values=(data['name_of_test'], message.from_user.id))

    await state.finish()
    await bot.send_message(message.from_user.id,"Нажмите на кнопку ниже и создайте викторину!", reply_markup=poll_keyboard)

async def on_create_poll_click(message: types.Message):
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []

        # Если юзер решил вручную отправить не викторину, а опрос, откажем ему.
    if message.poll.type != "quiz":
        await message.reply("Извините, я принимаю только викторины (quiz)!")
        return

        # Сохраняем себе викторину в память
    options = [o.text for o in message.poll.options]

    print(options)
    str_options = ""
    for i in range(len(options) - 1):
        str_options += str(options[i])
        str_options += ";;;"
    str_options += str(options[len(options) - 1])

    a = Database()
    id_tests = a.select_table("tests", "id_test", "name", name_test)
    print(id_tests)
    print(id_tests[0]["id_test"])
    values = (message.poll.id, message.chat.id,message.poll.question, str_options, message.poll.correct_option_id, id_tests[0]["id_test"])



    print(values)
    a.add_data("quizzes" , columns=["id_quiz", "chat_id", "question", "options","correct_option_id","id_tests"],
               values=values)

    print(str_options)
    tuple_list = str_options.split(";;;")
    print(tuple_list)


    # send
    # my_quiz = await bot.send_poll(chat_id=quizzes_database[str(message.from_user.id)][0].chat_id, question=message.poll.question,
    #                     is_anonymous=False, options=tuple_list, type="quiz",
    #                     correct_option_id=message.poll.correct_option_id)

    # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
    quizzes_owners[message.poll.id] = str(message.from_user.id)
    print("quizzes_database", quizzes_database)

    await message.reply(
        f"Викторина сохранена. Общее число сохранённых викторин: {len(quizzes_database[str(message.from_user.id)])}")

    # @dp.poll_answer_handler()
    # async def handle_poll_answer(quiz_answer: PollAnswer):
    #
    #     # подключение к бд
    #     # предположим, что res[0] - это вопрос, res[1] - верный ответ
    #     # все остальные ответы - неверные
    #
    #     # random.shuffle(data)
    #     if my_quiz.poll.correct_option_id == quiz_answer.option_ids[0]:
    #         # если ответ, который мы записали совпадает с тем, который выбрал юзер
    #         # тогда инкрементируем счетчик на +1
    #         await message.reply("правильно")
    #     else:
    #         await message.reply("неправильно")
    #     # инкрементируем счетчик отправленных викторин
    #     # если счетчик не равен 5, тогда отправляем следующую викторину
    #     # if count != 5:
    #     #     # перезаписываем верный ответ для следующей проверки викторины
    #     #     bot.send_poll(chat_id=message.user.id, question=res[0],
    #     #                   is_anonymous=False, options=data, type="quiz",
    #     #                   correct_option_id=data.index(res[1]))
    #     # else:
    #     #     bot.send_message(message.user.id,
    #     #              f'Тестирование завершено.\nВерных ответов {correct_count} из 5.')




def register_handlers_teacher(dp: Dispatcher):
    dp.register_message_handler(on_teacher_click, commands=['вчитель'], state=None)
    dp.register_message_handler(get_login, state=Reg_teacher.login)
    dp.register_message_handler(get_password, state=Reg_teacher.password)
    dp.register_message_handler(get_pin_cod, state=Reg_teacher.pin_cod)
    dp.register_message_handler(on_create_click, commands=['cтворити_тест'])
    dp.register_message_handler(get_name_of_test, state=Reg_name_of_test.name_of_test)
    dp.register_message_handler(on_create_poll_click, content_types=["poll"])
    dp.register_message_handler(on_register_click, commands=['реєстрація'])
    dp.register_message_handler(on_enter_click, commands=['вхід'])
    dp.register_message_handler(get_enter_login , state=Enter_teacher.login)
    dp.register_message_handler(get_enter_password, state=Enter_teacher.password)
    dp.register_message_handler(on_save_test, commands=['Start'])



