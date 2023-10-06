from telebot import types


def create_language_markup():
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton("РУ 🇷🇺", callback_data="RUS")
    bt2 = types.InlineKeyboardButton("ENG 🇬🇧", callback_data="ENG")
    markup.add(bt1, bt2, row_width=2)
    return markup
