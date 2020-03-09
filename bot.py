from telebot import TeleBot
import data_base
import markups as mk

bot = TeleBot('1107223113:AAEx7XU3s4vLbEpyfTMk7_73lLA1KtQi-Mc')

groups = ["6.1219-2"]
sub_groups = ["1", "2"]

@bot.message_handler(commands=['start'])
def hello(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Приветсвую!')
    msg = bot.send_message(chat_id, 'Введите вашу группу:', reply_markup=mk.choose_item(groups))
    bot.register_next_step_handler(msg, take_group)


@bot.message_handler()
def take_group(message):
    chat_id = message.chat.id
    group = message.text
    msg = bot.send_message(chat_id, 'Выберите подгруппу:', reply_markup=mk.choose_item(sub_groups))
    bot.register_next_step_handler(msg, take_sub_group, group)


@bot.message_handler()
def take_sub_group(message, group):
    username = message.from_user.username
    chat_id = message.chat.id
    sub_group = message.text
    group = group

    if message.from_user.username == 'Arty401' or message.from_user.username == "ErmishinD":
        is_admin = True
    else:
        is_admin = False

    data_base.User(chat_id=chat_id, username=username, action_flag='main',
                   is_admin=True, group=group, sub_group=sub_group).add_to_base()

    msg = bot.send_message(chat_id, 'Ваша группа: {0} ({1})\nПоздравляю! Вы успешно зарегистрировались.'.format(group, sub_group), reply_markup=mk.main())


bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

bot.polling(none_stop=True)
