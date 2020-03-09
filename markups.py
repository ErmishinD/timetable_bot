from telebot import types


def choose_item(items):
    '''выбор факультета/специальности/группы/курса'''
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for item in items:
        markup.row(types.KeyboardButton(item))

    markup.row("Отмена")
    return markup


def main():
    """маркап главного меню"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    buttons = ["Показать расписание",
               "Установить напоминание",
               "Какая сейчас пара?",
               "Как зовут преподавателя?",
               "Расписание другой группы"]
    for btn in buttons:
        markup.row(types.KeyboardButton(btn))
    return markup


def show_timetable():
    """подменю показа расписания"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    buttons = ["На сегодня",
               "На завтра",
               "Не неделю",
               "Расписание звонков"]
    for btn in buttons:
        markup.row(types.KeyboardButton(btn))
    return markup


def cancel():
    """маркап отмены"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Отмена")
    markup.row(btn1)
    return markup


def name_teacher():
    """подменю ФИО преподавателя"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    buttons = ["Сейчас",
               "Указать предмет",
               "Отмена"]
    for btn in buttons:
        markup.row(types.KeyboardButton(btn))
    return markup
