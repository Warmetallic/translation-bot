from decouple import config
import telebot
import requests
import json


# Getting secret keys from decouple
bot_key = config("BOT_KEY")
api_key = config("API_KEY")

bot = telebot.TeleBot(bot_key)

# DeepL API endpoint
deepl_api_endpoint = "https://api-free.deepl.com/v2/translate"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "test")


@bot.message_handler(content_types=["text"])
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


bot.infinity_polling()
