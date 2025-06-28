import telebot
import random

from telebot import types

token = "7655856956:AAHkaGPU2KZWvHMmStMcSnQHUB2knGIgDo8"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Okay Hello, you good, welcome to me!")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items1 = types.KeyboardButton("Привет!")
    items2 = types.KeyboardButton("Рандомное число")

    markup.add(items1, items2 )

    bot.reply_to(message, f"Welcome {message.from_user.first_name}!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def message(message):
    if message.chat.type == 'private':
        if message.text == 'Привет!':
            bot.send_message(message.chat.id, "Привет")
        elif message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        else:
            bot.send_message(message.chat.id, "Я не понял тебя :(")

bot.infinity_polling()
