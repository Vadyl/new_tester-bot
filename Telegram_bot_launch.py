'''main file '''


from create_bot import dp
from aiogram.utils import executor
# import handlers


from handlers import  student_interface ,teacher_interface , help , start

async def on_startup(_):
	print('Бот вышел в онлайн')

start.register_handlers_client(dp)
student_interface.register_handlers_client(dp)
teacher_interface.register_handlers_teacher(dp)
help.register_handlers_client(dp)


# teacher = KeyboardButton("/вчитель")
# student = KeyboardButton("/учень")
#
# start_buttons = ReplyKeyboardMarkup()
# start_buttons.add(teacher).add(student)


if __name__ == '__main__':
    # executor.start_polling(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)