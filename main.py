import random
import telebot

bot = telebot.TeleBot('6121496411:AAFNZJ03UKSnvWwdHn_C4hPCMXOt0accJa0')
flag = None
sweets = 60
max_sweets_count = 28


@bot.message_handler(commands=["start"])
def start(message):
    global flag
    bot.send_message(message.chat.id, f"Вы в игре!")
    flag = random.choice(["user", "bot"])
    bot.send_message(message.chat.id, f"Всего в игре {sweets} конфет")
    if flag == "user":
        bot.send_message(message.chat.id,
                         f"Первым ходите Вы")  # отправка сообщения (кому отправляем, что отправляем(str))
    else:
        bot.send_message(message.chat.id,
                         f"Первым ходит Бот")  # отправка сообщения (кому отправляем, что отправляем(str))
    controller(message)


def controller(message):
    global flag
    if sweets > 0:
        if flag == "user":
            bot.send_message(message.chat.id, f"Ваш ход. Введите количество конфет от 0 до {max_sweets_count}")
            bot.register_next_step_handler(message, user_input)
        else:
            bot_input(message)
    else:
        flag = "user" if flag == "bot" else "bot"
        bot.send_message(message.chat.id, f"Победил {flag} !")


def bot_input(message):
    global sweets, flag
    if sweets <= max_sweets_count:
        bot_turn = sweets
    elif sweets % max_sweets_count == 0:
        bot_turn = max_sweets_count - 1
    else:
        bot_turn = sweets % max_sweets_count - 1
    sweets -= bot_turn
    bot.send_message(message.chat.id, f"Бот взял {bot_turn} конфет")
    bot.send_message(message.chat.id, f"Осталось {sweets}")
    flag = "user" if flag == "bot" else "bot"
    controller(message)


def user_input(message):
    global sweets, flag
    user_turn = int(message.text)
    sweets -= user_turn
    bot.send_message(message.chat.id, f"Осталось {sweets}")
    flag = "user" if flag == "bot" else "bot"
    controller(message)


bot.infinity_polling()
