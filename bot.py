from telebot import TeleBot
import datetime
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


def format_pair(item):
    text = ""
    text += item[1] + " ~ " + item[2] + " - " + item[3]
    text += " в " + item[4] + " ауд.(" + item[5] + ") - "
    text += item[6] + ", которую ведет " + item[7] +"\n\n"
    return text


def format_week_query(query, current_day=""):
    text = ""

    if current_day == "":
        current_day = query[0][0]
        text += current_day.upper() + ":\n"

        for item in query:
            if item[0] == current_day:
                text += format_pair(item)
            else:
                current_day = item[0]
                text += "\n\n" + current_day.upper() + ":\n"
                text += format_pair(item)
        return text
    else:
        day_name = {0:"понедельник",
                    1:"вторник",
                    2:"среда",
                    3:"четверг",
                    4:"пятница",
                    5:"суббота",
                    6:"воскресенье"}
        current_day = day_name[current_day]
        text += current_day.upper() + ":\n"
        for item in query:
            if item[0] == current_day:
                text += format_pair(item)
        return text


def get_current_week_form():
    if (datetime.datetime.now().isocalendar()[1]) % 2 == 0:
        return "числитель"
    else:
        return "знаменатель"



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
        data_base.User(chat_id=chat_id, username=username,
                       is_admin=is_admin, group=group, sub_group=sub_group).add_to_base()
        bot.send_message(chat_id,
                         'Ваша группа: {0} ({1})\nПоздравляю! Вы успешно зарегистрировались.'.format(group, sub_group),
                         reply_markup=mk.main())
    else:
        bot.send_message(chat_id, 'Вы уже зарегистрированы!')


@bot.message_handler(content_types=['text'])
def change_group(message):
    chat_id = message.chat.id
    if message.text == 'Изменить группу':
        msg = bot.send_message(chat_id, 'Выбирай группу:', reply_markup=mk.choose_item(groups))
        bot.register_next_step_handler(msg, take_group)
    elif message.text == 'Показать расписание':
        msg = bot.send_message(chat_id, 'Какое расписание Вас интересует?', reply_markup=mk.show_timetable())
        bot.register_next_step_handler(msg, choose_timetable)
    elif message.text == 'Как зовут преподавателя?':
        msg = bot.send_message(chat_id, 'Какой преподаватель?', reply_markup=mk.name_teacher())
        bot.register_next_step_handler(msg, choose_teacher)
    else:
        bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())


@bot.message_handler()
def take_group(message):
    chat_id = message.chat.id
    new_group = message.text
    if check_cancel(new_group):
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
        data_base.User.change_sub_group(chat_id=chat_id, new_sub_group=new_sub_group)
        bot.send_message(chat_id, f'Ваша подгруппа изменена на {new_sub_group}', reply_markup=mk.main())
    else:
        msg = bot.send_message(chat_id, "Выбирай группу:", reply_markup=mk.choose_item(groups))
        bot.register_next_step_handler(msg, take_group)



@bot.message_handler()
def choose_timetable(message):
    chat_id = message.chat.id
    timetable_needed = message.text

    group = data_base.User.get_group(chat_id)
    sub_group = data_base.User.get_sub_group(chat_id)
    
    if check_cancel(timetable_needed):

        current_week_form = get_current_week_form()

        if message.text == "Не неделю":
            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            result = format_week_query(query)
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        elif message.text == "На сегодня":
            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            result = format_week_query(query, current_weekday)
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        elif message.text == "На завтра":
            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            result = format_week_query(query, current_weekday+1)
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        else:
            bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


@bot.message_handler()
def choose_teacher(message):
    chat_id = message.chat.id
    timetable_needed = message.text
    if check_cancel(timetable_needed):
        bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


# bot.enable_save_next_step_handlers()
# bot.load_next_step_handlers()

bot.polling(none_stop=True)
