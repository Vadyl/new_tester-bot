from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType, PollType, \
    InlineKeyboardButton, InlineKeyboardMarkup


def get_list_of_tests_button(test_names):


    # test_names_KeyboardButtons = []
    #
    # for i in test_names:
    #     test_names_KeyboardButtons.append(KeyboardButton(i))

    create_test_names =InlineKeyboardMarkup()  # resize_keyboard=True

    for i in test_names:

        create_test_names.add(InlineKeyboardButton(i, callback_data=i))

    return create_test_names


