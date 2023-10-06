from decouple import config
import telebot
from telebot import types
import requests
import json
from keyboards.inline_markup import create_language_markup


# Getting secret keys from decouple
bot_key = config("BOT_KEY")
api_key = config("API_KEY")

bot = telebot.TeleBot(bot_key)

# DeepL API endpoint
deepl_api_endpoint = "https://api-free.deepl.com/v2/translate"


@bot.message_handler(commands=["translate"])
def start(message):
    markup = create_language_markup()
    bot.send_message(
        message.chat.id,
        "Выберите на какой язык хотите перевести текст:\nChoose which language you need to translate into:",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["photo"])
def get_text(message):
    input_text = message.text.strip().lower()

    # Specify the parameters for the DeepL API request
    params = {
        "auth_key": api_key,  # Your DeepL API key
        "text": input_text,
        "target_lang": "ru",  # Target language (e.g., Russian)
    }

    # Make a GET request to the DeepL API
    res = requests.get(deepl_api_endpoint, params=params)

    if res.status_code == 200:
        data = json.loads(res.text)
        translated_text = data["translations"][0]["text"]
        bot.reply_to(message, translated_text)
    else:
        bot.reply_to(message, "Translation failed. Please try again later.")


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


def translate_function(message, target_lang):
    user_input = message.text
    params = {
        "auth_key": api_key,
        "text": user_input,
        "target_lang": target_lang,
    }

    res = requests.get(deepl_api_endpoint, params=params)

    if res.status_code == 200:
        data = json.loads(res.text)
        translated_text = data["translations"][0]["text"]
        bot.send_message(
            message.chat.id,
            f"Translation: {translated_text}",
            reply_markup=create_language_markup(),
        )

    else:
        bot.send_message(
            message.chat.id,
            "Translation failed. Please try again later.",
        )


bot.infinity_polling()
