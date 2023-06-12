import psycopg2
from environs import Env
from lexicon.lexicon_ru import LEXICON_CARD_RARE

env = Env()
env.read_env()

# Функция подключения к базе
def postreSQL_connect():
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        connect.autocommit = True
        with connect.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                           "id BIGSERIAL NOT NULL PRIMARY KEY,"
                           "user_id VARCHAR(30) NOT NULL,"
                           "login VARCHAR(50) NOT NULL,"
                           "universe VARCHAR(50) NOT NULL,"             # Наименование вселенной
                           "sum_dust VARCHAR(50) NOT NULL,"             # количество пыли 
                           "attempts VARCHAR(50) NOT NULL);")           # количество попыток

        with connect.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS cards ("
                           "id BIGSERIAL NOT NULL PRIMARY KEY,"
                           "name VARCHAR(50) NOT NULL,"
                           "img VARCHAR(100) NOT NULL,"    
                           "rare VARCHAR(50) NOT NULL,"                 # Редкость
                           "attack VARCHAR(50) NOT NULL,"         # атака 
                           "protection VARCHAR(50) NOT NULL,"         # защита 
                           "value VARCHAR(50) NOT NULL);")              # Ценность

        with connect.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS user_cards ("
                           "id BIGSERIAL NOT NULL PRIMARY KEY,"
                           "user_id VARCHAR(50) NOT NULL,"
                           "name_card VARCHAR(100) NOT NULL);")

        with connect.cursor() as cursor:
             cursor.execute("CREATE TABLE IF NOT EXISTS name_universes ("
                           "id BIGSERIAL NOT NULL PRIMARY KEY,"
                           "name VARCHAR(50) NOT NULL);")



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


def postreSQL_users(user_id):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM users WHERE user_id = '{user_id}';")
            user = cursor.fetchone()
            return user



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

def postreSQL_login(login):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM users WHERE login = '{login}';")
            login = cursor.fetchone()
            return login



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

def postreSQL_user_add(user_id, login):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"INSERT INTO users (user_id, login, status,universe, sum_dust, attempts) VALUES ('{user_id}',"
                                                                                                    f"'{login}',"
                                                                                                    f"'user',"
                                                                                                    f"'None',"
                                                                                                    f"'0',"
                                                                                                    f"'0');")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

#Функция добавления новой карточки
def postreSQL_card_add(card):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        value_card = 0
        if card['rare'] == LEXICON_CARD_RARE['usual']:
            value_card = 500
        elif card['rare'] == LEXICON_CARD_RARE['rare']:
            value_card = 1500
        elif card['rare'] == LEXICON_CARD_RARE['epic']:
            value_card = 6000
        elif card['rare'] == LEXICON_CARD_RARE['mythical']:
            value_card = 12000
        elif card['rare'] == LEXICON_CARD_RARE['legendary']:
            value_card = 30000

        with connect.cursor() as cursor:
            cursor.execute(f"INSERT INTO cards (name, img, rare, attack, protection, value) VALUES ('{card['neme']}',"
                                                                                                    f"'{card['img']}',"
                                                                                                    f"'{card['rare']}',"
                                                                                                    f"'{card['attack']}',"
                                                                                                    f"'{card['protection']}',"
                                                                                                    f"'{value_card}');")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

def postreSQL_admin(user_id):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM users WHERE user_id = '{user_id}' AND status = 'admin';")
            admin = cursor.fetchone()
            return admin



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

def postreSQL_cards(category):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{category}';")
            cards = cursor.fetchall()
            return cards



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
