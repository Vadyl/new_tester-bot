from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, PollType, \
    InlineKeyboardButton, InlineKeyboardMarkup


def get_list_of_tests_button(test_names):



    create_test_names =InlineKeyboardMarkup()

    for i in test_names:

        create_test_names.add(InlineKeyboardButton(i, callback_data=i))

    return create_test_names


