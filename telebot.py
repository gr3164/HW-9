# Задача 1. Добавьте telegram-боту возможность вычислять выражения:1 + 4 * 2 -> 9
# Задача 2. Добавьте в бота игру «Угадай числа». Бот загадывает число от 1 до 1000. 
# Когда игрок угадывает его, бот выводит количество сделанных ходов.

import telebot
from telebot import types
from random import randint

Dictionary = {}

def Init_d(user_id):
	Dictionary[user_id] = dict(count=None, random_number=None)

def Dictionary_add_content(user_id, key, value):
	Dictionary[user_id][key] = value

def print_d(user_id, key):
	return Dictionary[user_id][key]

count = 1



TOKEN = ""
bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def Hello_user(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(types.KeyboardButton('Калькулятор'), types.KeyboardButton('Игра'))
	bot.send_message(message.chat.id, text=f'Привет {message.chat.first_name}', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Калькулятор")
def Calc(message):
	bot.send_message(message.chat.id, text=f"Введите пример")
	if message.text == "Игра":
		bot.register_next_step_handler(message, Welcome_screen)
	else:
		bot.register_next_step_handler(message, Result)

def Result(message):
	if message.text == "Игра":
		bot.register_next_step_handler(message, Welcome_screen)
	else:
		user_number = message.text
		try:
			if str(eval(user_number)).isdigit():
				msg= bot.reply_to(message, str(eval(user_number)))
				bot.send_message(message.chat.id, text=f"Введите пример")
				bot.register_next_step_handler(msg, Result)
		except:
			msg = bot.send_message(message.chat.id, text=f'Ошибка!!!\nВведите число')
			bot.register_next_step_handler(message, Welcome_screen)


@bot.message_handler(func=lambda message: message.text == "Игра")
def Welcome_screen(message):
	global count
	Init_d(message.chat.id)

	count = 1
	random_number = randint(1, 1000)

	bot.send_message(message.chat.id, text=f"Игра «Угадай числа»\nЗагадоно число от 1 до 1000\nВведите число")
	Dictionary_add_content(message.chat.id, "count", count)
	Dictionary_add_content(message.chat.id, "random_number", random_number)
	bot.register_next_step_handler(message, Game)

def Game(message):
	global count

	if message.text.isdigit():
		user_number = int(message.text)
		print(print_d(message.chat.id, "random_number"))
		if user_number == Dictionary[message.chat.id]["random_number"]:
			bot.send_message(message.chat.id, text=f'Победа!!!\nЗагаданое число {user_number}')
			bot.send_message(message.chat.id, text=f'Было попыток: {print_d(message.chat.id, "count")}')
			Init_d(message.chat.id)
		elif user_number > Dictionary[message.chat.id]["random_number"]:
			count += 1
			bot.send_message(message.chat.id, text=f'Меньше')
			Dictionary_add_content(message.chat.id, "count", count)
			bot.register_next_step_handler(message, Game)
		elif user_number < Dictionary[message.chat.id]["random_number"]:
			count += 1
			bot.send_message(message.chat.id, text=f'Больше')
			Dictionary_add_content(message.chat.id, "count", count)
			bot.register_next_step_handler(message, Game)
	elif message.text == "Калькулятор":
		Init_d(message.chat.id)
		bot.register_next_step_handler(message, Calc)
	else:
		msg = bot.send_message(message.chat.id, text=f'Ошибка!!!\nВведите число')
		bot.register_next_step_handler(msg, Game)

bot.infinity_polling(none_stop=True, interval=0)