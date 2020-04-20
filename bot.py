from telebot import TeleBot
import datetime
import data_base
import markups as mk

bot = TeleBot('1107223113:AAEx7XU3s4vLbEpyfTMk7_73lLA1KtQi-Mc')

groups = ["6.1219-2"]
sub_groups = ["1", "2"]

week_days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]


def get_current_week_day(current_day):
    """Определение текущего дня недели"""
    day_name = {0:"понедельник",
                1:"вторник",
                2:"среда",
                3:"четверг",
                4:"пятница",
                5:"суббота",
                6:"воскресенье"}
    current_day = current_day % 7
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
    if item:
        text += item[1] + " ~ " + item[2] + " - " + item[3]
        text += " в " + item[4] + " ауд.(" + item[5] + ") - "
        text += item[6] + ", которую ведет " + item[7] + "\n\n"
    return text


def format_day_query(query, week_day):
    """Отформатировать расписание на день"""
    text = week_day.upper() + ":\n"
    
    if query:
        for item in query:
            if item[0] == week_day:
                text += format_pair(item)
            else:
                week_day = item[0]
                text += "\n\n" + week_day.upper() + ":\n"
                text += format_pair(item)
    else:
        text += "В этот день у Вас выходной!"
    return text


def format_week_query(query):
    """Отформатировать расписание на неделю"""
    text = ""

    current_day = query[0][0]
    text += current_day.upper() + ":\n"
    for item in query:
        if item[0] != current_day:
            current_day = item[0]
            text += "\n\n" + current_day.upper() + ":\n"
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


def get_time_start_end():
    # преобразовать строки массива во время (час, минута)
    time_start = ["8-00", "9-35", "11-25", "12-55", "14-30", "16-05", "17-40", "19-10"]
    time_end = ["9-20", "10-55", "12-45", "14-15", "15-50", "17-25", "19-00", "20-30"]
    for i in range(len(time_start)):
        time_start[i] = time_start[i].split("-")
        time_end[i] = time_end[i].split("-")
        
        time_start[i] = datetime.time(hour=int(time_start[i][0]), minute=int(time_start[i][1]), second=0)
        time_end[i] = datetime.time(hour=int(time_end[i][0]), minute=int(time_end[i][1]), second=0)
    return [time_start, time_end]


def get_str_time_start_end(time_start, time_end, i):
    pair_start = str(time_start[i].hour) + "-" + format_minute(str(time_start[i].minute))
    pair_end = str(time_end[i].hour) + "-" + format_minute(str(time_end[i].minute))
    return [pair_start, pair_end]


def get_next_week_day_form(week_day, week_form):
    current_week_day_number = week_days.index(week_day) + 1
    if current_week_day_number >= len(week_days):
        current_week_day_number = current_week_day_number % len(week_days)
        if week_form == "числитель":
            week_form = "знаменатель"
        else:
            week_form = "числитель"
    week_day = week_days[current_week_day_number]

    return [week_day, week_form]


def get_formated_current_pair(chat_id, group, sub_group, week_form, week_day):
    # TODO
    # оптимизировать данную функцию
    """Отформатировать текущую пару"""
    text = ""

    # узнать текущее время
    now = datetime.datetime.now()
    current_time = datetime.time(hour=now.hour, minute=now.minute)

    # получить два массива с временем (час, минута)
    time_start, time_end = get_time_start_end()

    # найти текущую пару (которая идет в данный момент)
    pair_found = False
    for i in range(len(time_start)):
        if time_start[i] <= current_time <= time_end[i]:
            pair_found = True
            # получить две строки с временем
            pair_start, pair_end = get_str_time_start_end(time_start, time_end, i)

            text += "Сейчас:\n"
            query = data_base.Pair.get_current_pair(chat_id, group, sub_group,
                                                    week_form, week_day, pair_start, pair_end)
            if query:
                text += format_pair(query[0])
            else:
                while not query:
                    i += 1
                    if i >= len(time_start):
                        i = 0
                        week_day, week_form = get_next_week_day_form(week_day, week_form)
                    
                    pair_start, pair_end = get_str_time_start_end(time_start, time_end, i)
                    query = data_base.Pair.get_current_pair(chat_id, group, sub_group,
                                                            week_form, week_day, pair_start, pair_end)
                text = "Следующая пара:\n"
                text += week_day.upper() + ":\n\n"
                text += format_pair(query[0])
                
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
            week_day = week_days[(week_days.index(week_day)+1) % 7]

        # преобразование времени (час, минута) в строки
        pair_start = str(time_start[i+1].hour) + "-" + format_minute(str(time_start[i+1].minute))
        pair_end = str(time_end[i+1].hour) + "-" + format_minute(str(time_end[i+1].minute))
        
        text += "Следующая пара:\n"
        query = data_base.Pair.get_current_pair(chat_id, group, sub_group, week_form, week_day, pair_start, pair_end)
        
        if query:
            text += format_pair(query[0])
        else:
            while not query:
                    i += 1
                    if i >= len(time_start):
                        i = 0
                        week_day, week_form = get_next_week_day_form(week_day, week_form)
                    
                    pair_start, pair_end = get_str_time_start_end(time_start, time_end, i)
                    query = data_base.Pair.get_current_pair(chat_id, group, sub_group, week_form, week_day, pair_start, pair_end)
            text += week_day.upper() + ":\n\n"
            text += format_pair(query[0])
    return text


def get_formated_teacher(teachers):
    uniqe_teachers = []

    for teacher in teachers:
        if teacher not in uniqe_teachers:
            uniqe_teachers.append(teacher)

    text = ""
    for teacher in uniqe_teachers:
        text += f'{teacher[0]} ведет {teacher[1]}.\n\n'

    return text


def get_formated_all_pairs(all_pairs):
    uniqe_pairs = []

    for pair in all_pairs:
        if pair[0] != '-' and pair[0] not in uniqe_pairs :
            uniqe_pairs.append(pair[0])

    return uniqe_pairs



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
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            current_weekday = get_current_week_day(current_weekday)
            if current_weekday == "воскресенье":
                if current_week_form == "числитель":
                    current_week_form = "знаменатель"
                else:
                    current_week_form = "числитель"

            query = data_base.Pair.get_week_schedule(chat_id, group, sub_group, current_week_form)
            result = format_week_query(query)
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        
        elif message.text == "На сегодня":
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            current_weekday = get_current_week_day(current_weekday)
            query = data_base.Pair.get_day_schedule(chat_id, group, sub_group, current_week_form, current_weekday)
            result = format_day_query(query, current_weekday)
            msg = bot.send_message(chat_id, result, reply_markup=mk.show_timetable())
            bot.register_next_step_handler(msg, choose_timetable)
        
        elif message.text == "На завтра":
            current_weekday = datetime.datetime.weekday(datetime.datetime.now())
            current_weekday = get_current_week_day(current_weekday+1)
            if current_weekday == "воскресенье":
                if current_week_form == "числитель":
                    current_week_form = "знаменатель"
                else:
                    current_week_form = "числитель"
            query = data_base.Pair.get_day_schedule(chat_id, group, sub_group, current_week_form, current_weekday)
            result = format_day_query(query, current_weekday)
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
    group = data_base.User.get_group(chat_id)
    sub_group = data_base.User.get_sub_group(chat_id)
    current_week_form = get_current_week_form()
    current_weekday = get_current_week_day(datetime.datetime.weekday(datetime.datetime.now()))
    query = data_base.Pair.get_day_schedule(chat_id, group, sub_group, current_week_form, current_weekday)

    if message.text == 'Сейчас':
        if query:
            print(query)
            pair_name = query[0][3]
            bot.send_message(chat_id, data_base.Pair.give_teacher(chat_id, group, sub_group, pair_name))
            bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())
        else:
            bot.send_message(chat_id, "Сейчас пары нет.\nГлавное меню", reply_markup=mk.main())
    elif message.text == 'Указать предмет':
        # получить список всех предметов студента
        # использовать маркап choose_item (параметром передать список всех предметов)
        all_pairs = data_base.Pair.get_all_pairs(chat_id, group)
        all_pairs = get_formated_all_pairs(all_pairs)

        msg = bot.send_message(chat_id, "Выберите предмет:", reply_markup=mk.choose_item(all_pairs))
        bot.register_next_step_handler(msg, get_teacher_by_pair_name)
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


@bot.message_handler()
def get_teacher_by_pair_name(message):
    chat_id = message.chat.id
    pair_name = message.text
    group = data_base.User.get_group(chat_id)
    sub_group = data_base.User.get_sub_group(chat_id)

    if check_cancel(pair_name):
        teachers = data_base.Pair.give_teacher(chat_id, group, sub_group, pair_name)
        if teachers:
            teacher_result = get_formated_teacher(teachers)

            msg = bot.send_message(chat_id, teacher_result, reply_markup=mk.name_teacher())
            bot.register_next_step_handler(msg, choose_teacher)
        else:
            msg = bot.send_message(chat_id, "У Вас нет такого предмета...", reply_markup=mk.name_teacher())
            bot.register_next_step_handler(msg, choose_teacher)
    else:
        bot.send_message(chat_id, "Главное меню", reply_markup=mk.main())


# bot.enable_save_next_step_handlers()
# bot.load_next_step_handlers()

bot.polling(none_stop=True)
