from telebot import TeleBot
import data_base

bot = TeleBot('1107223113:AAEx7XU3s4vLbEpyfTMk7_73lLA1KtQi-Mc')


@bot.message_handler(commands=['start'])
def hello(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Приветсвую!')
    msg = bot.send_message(chat_id, 'Введите ваш факультет:')
    bot.register_next_step_handler(msg, take_faculty)


@bot.message_handler()
def take_faculty(message):
    data_base.Faculty(message.text).add_to_base()


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

bot.polling(none_stop=True)
