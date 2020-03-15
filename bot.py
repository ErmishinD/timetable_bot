from telebot import TeleBot
import data_base
import markups as mk

bot = TeleBot('1107223113:AAEx7XU3s4vLbEpyfTMk7_73lLA1KtQi-Mc')

groups = ["6.1219-2"]
sub_groups = ["1", "2"]


@bot.message_handler(commands=['start'])
def hello(message):
    chat_id = message.chat.id
    username = message.from_user.username
    group = '6.1219-2'
    sub_group = 2
    bot.send_message(chat_id, 'Приветсвую!')
    is_admin = False

    if message.from_user.username == 'Arty401' or message.from_user.username == "ErmishinD":
        is_admin = True
    else:
        is_admin = False

    data_base.User(chat_id=chat_id, username=username, action_flag='main',
                   is_admin=is_admin, group=group, sub_group=sub_group).add_to_base()

    bot.send_message(chat_id, 'Ваша группа: {0} ({1})\nПоздравляю! Вы успешно зарегистрировались.'.format(group, sub_group), reply_markup=mk.main())


@bot.message_handler(content_types=['text'])
def change_group(message):
    chat_id = message.chat.id
    if message.text == 'Изменить группу':
        data_base.User.change_action(chat_id, 'change_group_step_1')
        msg = bot.send_message(chat_id, 'Выбирай группу:')
        bot.register_next_step_handler(msg, take_group)


@bot.message_handler()
def take_group(message):
    chat_id = message.chat.id
    new_group = message.text
    data_base.User.change_action(chat_id, 'change_group_step_2')
    data_base.User.change_group(chat_id=chat_id, new_group=new_group)
    bot.send_message(chat_id, f'Ваша группа изменена на {new_group}')


# bot.enable_save_next_step_handlers()
# bot.load_next_step_handlers()

bot.polling(none_stop=True)
