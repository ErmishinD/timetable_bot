from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание объекта 'engine' для подключения к БД
engine = create_engine('sqlite:///data_base.db', echo=True)

# База для всех классов
Base = declarative_base()


class User(Base):
    """Инициализация класа и таблицы БД 'user'

    :param chat_id: id чата в телегараме.
    :type chat_id: int.
    :param username: Имя аккаунта юзера.
    :type username: str.
    :param action_flag: В каком меню бота сейчас находится человек.
    :type action_flag: str.
    :param is_admin: Проверка на админа (Я или Дима).
    :type is_admin: bool.
    :param group: Шифр группы.
    :type group: str.
    :param sub_group: Номер подгруппы.
    :type sub_group: int."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    action_flag = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    group = Column(String, nullable=False)
    sub_group = Column(Integer, nullable=False)

    def __init__(self, chat_id, username, action_flag, is_admin, group, sub_group):
        self.chat_id = chat_id
        self.username = username
        self.action_flag = action_flag
        self.is_admin = is_admin
        self.group = group
        self.sub_group = sub_group

    def __repr__(self):
        return "User<(%s, %s, %s, %s, %s, %s)>" % (self.chat_id, self.username, self.action_flag,
                                                   self.is_admin, self.group, self.sub_group)

    def add_to_base(self):
        session_make = sessionmaker(engine)
        session = session_make()

        add = User(chat_id=self.chat_id, username=self.username, action_flag=self.action_flag,
                   is_admin=self.is_admin, group=self.group, sub_group=self.sub_group)

        session.add(add)
        session.commit()


class Pair(Base):
    """Инициализация класса и таблицы в БД 'pair'.

    :param pair_name: Название пары.
    :type pair_name: str.
    :param form_of_pair: Вид пары (лекция, практика и т.д).
    :type form_of_pair: str.
    :param teacher: ФИО преподавателя.
    :type teacher: str.
    :param housing: Номер учебного корпуса.
    :type housing: int.
    :param lecture_hall: Номер аудитории.
    :type lecture_hall: int
    :param pair_start: Начало пары.
    :type pair_start: str.
    :param pair_end: Конец пары.
    :type pair_end: str.
    :param week_day: День недели.
    :type week_day: str.
    :param week_form: Числитель или знаменатель.
    :type week_form: str.
    :param faculty: Название факультета.
    :type faculty: string.
    :param course: Номер курса.
    :type course: int.
    :param group: Шифр группы.
    :type group: string.
    :param sub_group: Номер подгруппы.
    :type sub_group: int."""

    __tablename__ = 'pair'

    id = Column(Integer, primary_key=True, nullable=False)
    pair_name = Column(String, nullable=False)
    form_of_pair = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    housing = Column(String, nullable=False)
    lecture_hall = Column(String, nullable=False)
    pair_start = Column(String, nullable=False)
    pair_end = Column(Text, nullable=False)
    week_day = Column(String, nullable=False)
    week_form = Column(String, nullable=False)
    faculty = Column(String, nullable=False)
    course = Column(Integer, nullable=False)
    group = Column(String, nullable=False)
    sub_group = Column(Integer, nullable=False)

    def __init__(self, pair_name, form_of_pair, teacher, housing, lecture_hall,
                 pair_start, pair_end, week_day, week_form, 
                 faculty, course, group, sub_group):

        self.pair_name = pair_name
        self.form_of_pair = form_of_pair
        self.teacher = teacher
        self.housing = housing
        self.lecture_hall = lecture_hall
        self.pair_start = pair_start
        self.pair_end = pair_end
        self.week_day = week_day
        self.week_form = week_form
        self.faculty = faculty
        self.course = course
        self.group = group
        self.sub_group = sub_group

    def __repr__(self):
        return "Pair<('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
               " '%s', '%s', '%s', '%s', '%s')>" % (self.pair_name, self.form_of_pair,
                                                    self.teacher, self.housing,
                                                    self.lecture_hall,
                                                    self.pair_start, self.pair_end,
                                                    self.week_day, self.week_form,
                                                    self.faculty, self.course,
                                                    self.group, self.sub_group)

    def add_to_base(self):
        session_make = sessionmaker(engine)
        session = session_make()

        add = Pair(pair_name=self.pair_name, form_of_pair=self.form_of_pair, teacher=self.teacher, housing=self.housing,
                   lecture_hall=self.lecture_hall, pair_start=self.pair_start, pair_end=self.pair_end,
                   week_day=self.week_day, week_form=self.week_form, faculty=self.faculty, course=self.course,
                   group=self.group, sub_group=self.sub_group)

        session.add(add)
        session.commit()


# Создание всех таблиц
Base.metadata.create_all(engine)

# Пример добавления в базу
# Pair(_данные_).add_to_base()

