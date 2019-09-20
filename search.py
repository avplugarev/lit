import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import user as usr


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):

    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def ask():
    user_id = input("Введи идентификатор пользователя: ")
    return int(user_id)

def convert_str_to_date(date_str):
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def close_by_bd(user, session):
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None
    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd

    return athlete_id, athlete_bd


def close_by_height(user, session):
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height

    return athlete_id, athlete_height
def main():

    session = usr.connect_db()
    user_id = ask()
    user = session.query(Athelete).filter(Athelete.id == user_id).first()
    print("Исхрдные данные для id ={id} c датой {date} и ростом {height}".format(id=user.id,
                                                                        date=user.birthdate,
                                                                        height=user.height))
    if not user:
        print("Мимо")
    else:
        bd_athlete, bd = close_by_bd(user, session)
        height_athlete, height = close_by_height(user, session)
        print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd))
        print("Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height))


if __name__ == "__main__":
    main()
