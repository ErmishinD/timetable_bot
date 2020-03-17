from telebot import TeleBot
import data_base
import markups as mk

bot = TeleBot('1107223113:AAEx7XU3s4vLbEpyfTMk7_73lLA1KtQi-Mc')

groups = ["6.1219-2"]
sub_groups = ["1", "2"]


def check_cancel(text):
    if text == "Отмена":
        return False
    else:
        return True


def format_week_query(query):
    text = ""

    current_day = query[0][0]
    text += current_day.upper() + ":\n"

    for item in query:
        if item[0] == current_day:
            text += item[1] + " ~ " + item[2] + " - " + item[3]
            text += " в " + item[4] + " ауд.(" + item[5] + ") - "
            text += item[6] + ", которую ведет " + item[7] +"\n"
        else:
            current_day = item[0]
            text += "\n" + current_day.upper() + ":\n"
            text += item[1] + " ~ " + item[2] + " - " + item[3]
            text += " в " + item[4] + " ауд.(" + item[5] + ") - "
            text += item[6] + ", которую ведет " + item[7] +"\n"
    return text


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

    if data_base.User.check_in_base(chat_id):
        data_base.User(chat_id=chat_id, username=username, action_flag='main',
                       is_admin=is_admin, group=group, sub_group=sub_group).add_to_base()
        bot.send_message(chat_id,
                         'Ваша группа: {0} ({1})\nПоздравляю! Вы успешно зарегистрировались.'.format(group, sub_group),
                         reply_markup=mk.main())
    else:
        bot.send_message(chat_id, 'Вы уже зарегистрированы!')


@bot.message_handler(content_types=['text'])
def change_group(message):
    chat_id = message.chat.id
    data_base.User.change_action(chat_id, 'main')
    if message.text == 'Изменить группу':
        data_base.User.change_action(chat_id, 'change_group_step_1')
        msg = bot.send_message(chat_id, 'Выбирай группу:', reply_markup=mk.choose_item(groups))
        bot.register_next_step_handler(msg, take_group)
    elif message.text == 'Показать расписание':
        data_base.User.change_action(chat_id, 'show_timetable_step_1')
        msg = bot.send_message(chat_id, 'Какое расписание Вас интересует?', reply_markup=mk.show_timetable())
        bot.register_next_step_handler(msg, choose_timetable)
    elif message.text == 'Как зовут преподавателя?':
        data_base.User.change_action(chat_id, 'teacher_name_step_1')
        msg = bot.send_message(chat_id, 'Какой преподаватель?', reply_markup=mk.name_teacher())
        bot.register_next_step_handler(msg, choose_teacher)
    else:
        bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())


@bot.message_handler()
def take_group(message):
    chat_id = message.chat.id
    new_group = message.text
    if check_cancel(new_group):
        data_base.User.change_action(chat_id, 'change_group_step_2')
        data_base.User.change_group(chat_id=chat_id, new_group=new_group)
        msg = bot.send_message(chat_id, f'Ваша группа изменена на {new_group}\nТеперь выбирай подгруппу:', reply_markup=mk.choose_item(sub_groups))
        bot.register_next_step_handler(msg, take_sub_group)
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


@bot.message_handler()
def take_sub_group(message):
    chat_id = message.chat.id
    new_sub_group = message.text
    if check_cancel(new_sub_group):
        data_base.User.change_action(chat_id, 'change_group_step_3')
        data_base.User.change_sub_group(chat_id=chat_id, new_sub_group=new_sub_group)
        bot.send_message(chat_id, f'Ваша подгруппа изменена на {new_sub_group}', reply_markup=mk.main())
    else:
        msg = bot.send_message(chat_id, "Выбирай группу:", reply_markup=mk.choose_item(groups))
        bot.register_next_step_handler(msg, take_group)

    data_base.User.change_action(chat_id, 'main')


@bot.message_handler()
def choose_timetable(message):
    chat_id = message.chat.id
    timetable_needed = message.text
    data_base.User.change_action(chat_id, 'show_timetable_step_2')

    if check_cancel(timetable_needed):
        if message.text == "Не неделю":
            query = data_base.Pair.get_week_schedule(chat_id, "6.1219-2", 1, "числитель")
            result = format_week_query(query)
            bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
        else:
            bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())

@bot.message_handler()
def choose_teacher(message):
    chat_id = message.chat.id
    timetable_needed = message.text
    data_base.User.change_action(chat_id, 'teacher_name_step_2')
    if check_cancel(timetable_needed):
        bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


# bot.enable_save_next_step_handlers()
# bot.load_next_step_handlers()

bot.polling(none_stop=True)
