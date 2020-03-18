from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import update

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
    is_admin = Column(Boolean, nullable=False)
    group = Column(String, nullable=False)
    sub_group = Column(Integer, nullable=False)

    def __init__(self, chat_id, username, is_admin, group, sub_group):
        self.chat_id = chat_id
        self.username = username
        self.is_admin = is_admin
        self.group = group
        self.sub_group = sub_group

    def __repr__(self):
        return "User<(%s, %s, %s, %s, %s, %s)>" % (self.chat_id, self.username,
                                                   self.is_admin, self.group, self.sub_group)

    def add_to_base(self):
        session_make = sessionmaker(engine)
        session = session_make()

        add = User(chat_id=self.chat_id, username=self.username,
                   is_admin=self.is_admin, group=self.group, sub_group=self.sub_group)

        session.add(add)
        session.commit()

    def change_group(chat_id, new_group):
        """Функция изменения группы пользователя"""
        conn = engine.connect()  # Создания соединения с таблицей
        update_group = update(User).where(User.chat_id == chat_id).values(group=new_group)  # Обновление данных
        conn.execute(update_group)  # Выполнение команды
        conn.close()  # Закрытие соединения с таблицей

    def change_sub_group(chat_id, new_sub_group):
        """Функция изменения подгруппы пользователя"""
        conn = engine.connect()  # Создания соединения с таблицей
        update_sub_group = update(User).where(User.chat_id == chat_id).values(sub_group=new_sub_group)  # Обновление данных
        conn.execute(update_sub_group)  # Выполнение команды

    def check_in_base(chat_id):
        session_make = sessionmaker(engine)
        session = session_make()

        query = session.query(User.chat_id).filter(User.chat_id == chat_id).order_by(User.chat_id)
        query = query.scalar()
        print(query)

        if query == None:
            return True
        else:
            return False

    def get_group(chat_id):
        session_make = sessionmaker(engine)
        session = session_make()

        query = session.query(User.group).filter(User.chat_id == chat_id)
        query = query.scalar()

        print(query)
        return query


    def get_sub_group(chat_id):
        session_make = sessionmaker(engine)
        session = session_make()

        query = session.query(User.sub_group).filter(User.chat_id == chat_id)
        query = query.scalar()

        print(query)
        return query


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

    def get_week_schedule(chat_id, group, sub_group, week_form):
        session_make = sessionmaker(engine)
        session = session_make()

        query = session.query(Pair.week_day,
                              Pair.pair_start, Pair.pair_end,
                              Pair.pair_name, Pair.lecture_hall,
                              Pair.housing, Pair.form_of_pair,
                              Pair.teacher).filter(Pair.week_form == week_form).filter(Pair.pair_name != '-').filter(Pair.group == group).filter(Pair.sub_group == sub_group)
        query = list(query)
        return query

    def get_current_pair(chat_id, group, sub_group, week_form, week_day, pair_start, pair_end):
        session_make = sessionmaker(engine)
        session = session_make()

        query = session.query(Pair.week_day,
                              Pair.pair_start, Pair.pair_end,
                              Pair.pair_name, Pair.lecture_hall,
                              Pair.housing, Pair.form_of_pair,
                              Pair.teacher).filter(Pair.week_form == week_form).filter(Pair.pair_name != '-').filter(Pair.group == group).filter(Pair.sub_group == sub_group).filter(Pair.week_day == week_day).filter(Pair.pair_start == pair_start).filter(Pair.pair_end == pair_end)
        
        return query


# Создание всех таблиц
Base.metadata.create_all(engine)

# Пример добавления в базу
# Pair(_данные_).add_to_base()
