import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
db_path='sqlite:///sochi_athletes.sqlite3'
# базовый класс моделей таблиц
Base=declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__='user'
    #описываем таблицу
    id =sa.Column(sa.INTEGER, primary_key=True)
    first_name=sa.Column(sa.TEXT)
    last_name=sa.Column(sa.TEXT)
    gender =sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.FLOAT)

def connect_db():
    """
        Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
        """
    engine = sa.create_engine(db_path)
    Base.metadata.create_all(engine)
    session=sessionmaker(engine)
    return session()
def request_data():
    """
        Запрашивает у пользователя данные и добавляет их в список users
        """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Имя: ")
    last_name = input("Фамилию: ")
    gender = input("Пол: ")
    email = input("Адрес электронной почты: ")
    birthdate = input("Дата рождения: ")
    height = input("Рост: ")

    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name = last_name,
        email = email,
        gender = gender,
        birthdate = birthdate,
        height = height
    )
    return user

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")
if __name__ == "__main__":
    main()





