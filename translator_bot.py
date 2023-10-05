from decouple import config
import telebot
import requests
import json


# getting secret keys from decouple
bot_key = config("BOT_KEY")
api_key = config("API_KEY")

bot = telebot.TeleBot(bot_key)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "test")


bot.infinity_polling()
