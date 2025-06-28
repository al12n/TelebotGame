import telebot
import random
from telebot import types
import config

bot = telebot.TeleBot(config.token)

user_data = {}  # Для "Холодно горячо"
suefa_mode = {}  # Для Суефа (камень-ножницы-бумага)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Холодно горячо")
    btn2 = types.KeyboardButton("Суефа")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}! Во что хотите сыграть? Если хотите несколько раундов сыграть в Суефа напишите Суефа после каждого раунда', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def game(message):
    chat_id = message.chat.id
    text = message.text.lower()

    # ==== ХОЛОДНО-ГОРЯЧО ====
    if text == "холодно горячо":
        number = random.randint(1, 100)
        user_data[chat_id] = number
        bot.send_message(chat_id, 'Я загадал число от 1 до 100! Попробуй угадать!')

    elif chat_id in user_data:
        try:
            guess = int(text)
            number = user_data[chat_id]

            if guess < number:
                bot.send_message(chat_id, "Мало!")
            elif guess > number:
                bot.send_message(chat_id, "Много!")
            else:
                bot.send_message(chat_id, f"🎉 Угадал! Это было {number}!")
                del user_data[chat_id]
        except ValueError:
            pass  # Если не число — игнорируем, может идёт другая игра

    # ==== СУЕФА ====
    if text == "суефа":
        suefa_mode[chat_id] = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Камень")
        btn2 = types.KeyboardButton("Ножницы")
        btn3 = types.KeyboardButton("Бумага")
        markup.add(btn1, btn2, btn3)
        bot.send_message(chat_id, "Выбери: Камень, Ножницы или Бумага", reply_markup=markup)

    elif suefa_mode.get(chat_id):
        user_choice = text
        choices = ["камень", "ножницы", "бумага"]
        if user_choice not in choices:
            bot.send_message(chat_id, "Выбери только Камень, Ножницы или Бумага!")
            return

        bot_choice = random.choice(choices)

        result = ""
        if user_choice == bot_choice:
            result = "Ничья!"
        elif (user_choice == "камень" and bot_choice == "ножницы") or \
             (user_choice == "ножницы" and bot_choice == "бумага") or \
             (user_choice == "бумага" and bot_choice == "камень"):
            result = "Ты выиграл! 🎉"
        else:
            result = "Ты проиграл... 😢"

        bot.send_message(chat_id, f"Ты выбрал: {user_choice.capitalize()}\n"
                                  f"Бот выбрал: {bot_choice.capitalize()}\n"
                                  f"{result}")
        suefa_mode.pop(chat_id)

    # ==== Если ни одна из игр ====
    elif chat_id not in user_data and not suefa_mode.get(chat_id):
        bot.send_message(chat_id, "Выбери игру: 'Холодно горячо' или 'Суефа'.")


bot.infinity_polling()
