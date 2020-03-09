from telebot import types


def main():
    '''маркап главного меню'''
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Показать расписание")
    btn2 = types.KeyboardButton("Установить напоминание")
    btn3 = types.KeyboardButton("Какая сейчас пара?")
    btn4 = types.KeyboardButton("Как зовут преподавателя?")
    btn5 = types.KeyboardButton("Расписание другой группы")

    buttons = [btn1, btn2, btn3, btn4, btn5]
    for btn in buttons:
        markup.row(btn)
    return markup


def show_timetable():
    '''подменю показа расписания'''
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("На сегодня")
    btn2 = types.KeyboardButton("На завтра")
    btn3 = types.KeyboardButton("Не неделю")
    btn4 = types.KeyboardButton("Расписание звонков")

    buttons = [btn1, btn2, btn3, btn4]
    for btn in buttons:
        markup.row(btn)
    return markup


def cancel():
    '''маркап отмены'''
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Отмена")
    murkup.row(btn1)
    return markup

def name_teacher():
    '''подменю ФИО преподавателя'''
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Сейчас")
    btn2 = types.KeyboardButton("Указать предмет")
    btn3 = types.KeyboardButton("Отмена")

    buttons = [btn1, btn2, btn3]
    for btn in buttons:
        markup.row(btn)
    return markup