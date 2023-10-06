from decouple import config
import telebot
import json
from keyboards.inline_markup import create_language_markup
from API.api_function import api_connect
from database.db_functions import (
    create_db,
    update_user,
    get_user_history,
    delete_user_history,
)


# Getting secret keys from decouple
bot_key = config("BOT_KEY")
api_key = config("API_KEY")

bot = telebot.TeleBot(bot_key)

# DeepL API endpoint
deepl_api_endpoint = "https://api-free.deepl.com/v2/translate"

# Create SQLite database
create_db()


# Main function to open menu for translation
@bot.message_handler(commands=["translate"])
def start(message):
    markup = create_language_markup()
    bot.send_message(
        message.chat.id,
        "Выберите на какой язык хотите перевести текст:\nChoose which language you need to translate into:",
        reply_markup=markup,
    )


# Handle the /history command
@bot.message_handler(commands=["history"])
def show_history(message):
    user_id = message.from_user.id
    history = get_user_history(user_id)

    if history:
        response = "Translation History:\n\n"
        for idx, entry in enumerate(history, 1):
            original_text = entry["original_text"]
            translated_text = entry["translated_text"]
            response += (
                f"{idx}. Original Text: {original_text}\nResult: {translated_text}\n\n"
            )
    else:
        response = "Translation History is empty."

    bot.send_message(message.chat.id, response)


# Handle the /delete_history command
@bot.message_handler(commands=["delete_history"])
def delete_history(message):
    user_id = message.from_user.id
    deleted_count = delete_user_history(user_id)

    if deleted_count > 0:
        response = f"Deleted {deleted_count} records from your Translation History."
    else:
        response = "No records found to delete in your Translation History."

    bot.send_message(message.chat.id, response)


# Handle callbacks from buttons
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if "RUS" in call.data:
        bot.send_message(call.message.chat.id, "Введите текст для перевода на русский:")
        # Set the callback state for this user to 'api'
        bot.register_next_step_handler(
            call.message, translate_function, target_lang="ru"
        )
    elif "ENG" in call.data:
        bot.send_message(
            call.message.chat.id, "Введите текст для перевода на английский:"
        )
        bot.register_next_step_handler(
            call.message, translate_function, target_lang="en"
        )


# Translate function, connects to API and return translated text
def translate_function(message, target_lang):
    user_input = message.text
    # request to Deepl's API
    res = api_connect(user_input, target_lang)

    if res.status_code == 200:
        data = json.loads(res.text)
        translated_text = data["translations"][0]["text"]
        bot.reply_to(
            message,
            f"Translation: {translated_text}",
            reply_markup=create_language_markup(),
        )
        update_user(message.from_user.id, user_input, translated_text)

    else:
        bot.reply_to(
            message,
            "Translation failed. Please try again later.",
        )


bot.infinity_polling()
