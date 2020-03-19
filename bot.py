from telebot import TeleBot
import datetime
import data_base
import markups as mk

bot = TeleBot('1107223113:AAEx7XU3s4vLbEpyfTMk7_73lLA1KtQi-Mc')

groups = ["6.1219-2"]
sub_groups = ["1", "2"]

week_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье", "понедельник"]


def get_current_week_day(current_day):
    """Определение текущего дня недели"""
    day_name = {0:"понедельник",
                    1:"вторник",
                    2:"среда",
                    3:"четверг",
                    4:"пятница",
                    5:"суббота",
                    6:"воскресенье"}
    current_day = day_name[current_day]
    return current_day


def check_cancel(text):
    """Проверка на то, была ли нажата кнопка 'Отмена' """
    if text == "Отмена":
        return False
    else:
        return True


def format_pair(item):
    """Отформатировать вывод информации о паре"""
    text = ""
    text += item[1] + " ~ " + item[2] + " - " + item[3]
    text += " в " + item[4] + " ауд.(" + item[5] + ") - "
    text += item[6] + ", которую ведет " + item[7] +"\n\n"
    return text


def format_week_query(query, current_day=""):
    """Отформатировать расписание на неделю"""
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
        text += current_day.upper() + ":\n"
        for item in query:
            if item[0] == current_day:
                text += format_pair(item)
        return text


def get_call_schedule():
    """Получить расписание звонков"""
    pair_number = list("12345678")
    time_start = ["8-00", "9-35", "11-25", "12-55", "14-30", "16-05", "17-40", "19-10"]
    time_end = ["9-20", "10-55", "12-45", "14-15", "15-50", "17-25", "19-00", "20-30"]
    
    text = ""
    for i, start, end in zip(pair_number, time_start, time_end):
        text += i + "-я пара с " + start + " до " + end + "\n"

    return text


def get_current_week_form():
    """Узнать какая сейчас неделя: числитель или знаменатель"""
    if (datetime.datetime.now().isocalendar()[1]) % 2 == 0:
        return "числитель"
    else:
        return "знаменатель"


def format_minute(minute):
    """Отформатировать текущие минуты для запросы в БД"""
    if len(minute) == 1:
        minute = "0" + minute
    return minute


def get_formated_current_pair(chat_id, group, sub_group, week_form, week_day):
    """Отформатировать текущую пару"""
    text = ""

    # узнать текущее время
    now = datetime.datetime.now()
    current_time = datetime.time(hour=now.hour, minute=now.minute)


    # преобразовать строки массива во время (час, минута)
    time_start = ["8-00", "9-35", "11-25", "12-55", "14-30", "16-05", "17-40", "19-10"]
    time_end = ["9-20", "10-55", "12-45", "14-15", "15-50", "17-25", "19-00", "20-30"]
    for i in range(len(time_start)):
        time_start[i] = time_start[i].split("-")
        time_end[i] = time_end[i].split("-")
        
        time_start[i] = datetime.time(hour=int(time_start[i][0]), minute=int(time_start[i][1]), second=0)
        time_end[i] = datetime.time(hour=int(time_end[i][0]), minute=int(time_end[i][1]), second=0)


    # найти текущую пару (которая идет в данный момент)
    pair_found = False
    for i in range(len(time_start)):
        if time_start[i] <= current_time <= time_end[i]:
            pair_found = True
            pair_start = str(time_start[i].hour) + "-" + format_minute(str(time_start[i].minute))
            pair_end = str(time_end[i].hour) + "-" + format_minute(str(time_end[i].minute))

            text += "Сейчас:\n"
            query = data_base.Pair.get_current_pair(chat_id, group, sub_group, week_form, week_day, pair_start, pair_end)
            if query != []:
                text += format_pair(query[0])
            else:
                # делать запросы в БД со следующим временем (если нужно, то мнять  на следующий день)
                # делать эти запросы до тех пор, пока не будет найдена пара (при этом указать день недели)
                pass
            break


    # если пара в данный момент не идет, то найти следующую
    if not pair_found:
        text += "В данный момент пара не идет. "

        # определить: сейчас идет перемена или нет? (ищется пара следующая после перемены)
        time_rest_end = list(time_start)
        offset = time_rest_end.pop(0)
        time_rest_end.append(offset)
        for i in range(len(time_rest_end)):
            if time_end[i] <= current_time <= time_rest_end[i]:
                pair_number = i
                pair_found = True
                break
        
        # искать пару в завтрашнем дне, если сегодня пар больше нет
        if not pair_found:
            i = 0
            week_day = week_days[week_days.index(week_day)+1]

        # преобразование времени (час, минута) в строки
        pair_start = str(time_start[i+1].hour) + "-" + format_minute(str(time_start[i+1].minute))
        pair_end = str(time_end[i+1].hour) + "-" + format_minute(str(time_end[i+1].minute))
        
        text += "Следующая пара:\n"
        query = data_base.Pair.get_current_pair(chat_id, group, sub_group, week_form, week_day, pair_start, pair_end)
        
        if query != []:
            text += format_pair(query[0])
        else:
            # делать запросы в БД со следующим временем (если нужно, то мнять  на следующий день)
            # делать эти запросы до тех пор, пока не будет найдена пара (при этом указать день недели)
            pass
    return text


@bot.message_handler(commands=['start'])
def hello(message):
    """Регистрация пользователя и занесение его в БД"""
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
    """ Обработка сообщений в главном меню"""
    chat_id = message.chat.id
    group = data_base.User.get_group(chat_id)
    sub_group = data_base.User.get_sub_group(chat_id)

    if message.text == 'Изменить группу':
        msg = bot.send_message(chat_id, 'Выбирай группу:', reply_markup=mk.choose_item(groups))
        bot.register_next_step_handler(msg, take_group)
    elif message.text == 'Показать расписание':
        msg = bot.send_message(chat_id, 'Какое расписание Вас интересует?', reply_markup=mk.show_timetable())
        bot.register_next_step_handler(msg, choose_timetable)
    elif message.text == 'Как зовут преподавателя?':
        msg = bot.send_message(chat_id, 'Какой преподаватель?', reply_markup=mk.name_teacher())
        bot.register_next_step_handler(msg, choose_teacher)
    elif message.text == 'Какая сейчас пара?':
        current_week_form = get_current_week_form()
        current_week_day = get_current_week_day(datetime.datetime.weekday(datetime.datetime.now()))

        result = get_formated_current_pair(chat_id, group, sub_group, current_week_form, current_week_day)
        bot.send_message(chat_id, result, reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())


@bot.message_handler()
def take_group(message):
    """ Изменение группы"""
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
    """Изменение подгруппы"""
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
    """Выбор типа расписания"""
    chat_id = message.chat.id

    group = data_base.User.get_group(chat_id)
    sub_group = data_base.User.get_sub_group(chat_id)
    current_week_form = get_current_week_form()
    
    if check_cancel(message.text):
        if message.text == "Не неделю":
            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            result = format_week_query(query)
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        
        elif message.text == "На сегодня":
            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            result = format_week_query(query, get_current_week_day(current_weekday))
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        
        elif message.text == "На завтра":
            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            result = format_week_query(query, get_current_week_day(current_weekday+1))
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        
        elif message.text == "Расписание звонков":
            call_schedule = get_call_schedule()
            msg = bot.send_message(chat_id, call_schedule, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        
        else:
            bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


@bot.message_handler()
def choose_teacher(message):
    """Узнать ФИО преподавателя"""
    chat_id = message.chat.id
    timetable_needed = message.text
    if check_cancel(timetable_needed):
        bot.send_message(chat_id, "Эта функция пока не реализована)", reply_markup=mk.main())
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


# bot.enable_save_next_step_handlers()
# bot.load_next_step_handlers()

bot.polling(none_stop=True)
