from datetime import datetime

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
                           "attempts VARCHAR(50) NOT NULL,"          # количество попыток
                           "status VARCHAR(10) NOT NULL,"          # количество попыток
                           "page VARCHAR(50),"           # страница
                           "chance_epic VARCHAR(10),"           # шанс эпический
                           "chance_mythical VARCHAR(10),"           # шанс мифической
                           "chance_legendary VARCHAR(10),"      # шанс легендарный
                           "data VARCHAR(50) NOT NULL);")

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

# Информация про юзера
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
#Проверка логина
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
#Добавление нового пользователя
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
            cursor.execute(f"INSERT INTO users (user_id, login, status, universe, sum_dust, attempts, page, chance_epic, chance_mythical, chance_legendary, data) "
                           f"VALUES ('{user_id}',"
                            f"'{login}',"
                            f"'user',"
                            f"'None',"
                            f"'0',"
                            f"'2',"
                            f"'0',"
                            f"'60',"
                            f"'30',"
                            f"'10',"
                           f"'{datetime.now()}');")

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

# функция обновления
def postreSQL_pg_up(user_id, pg):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT page FROM users WHERE user_id = '{user_id}'")
            pg_user = int(cursor.fetchone()[0][0])

        if pg == -2:
            with connect.cursor() as cursor:
                cursor.execute(
                    f"UPDATE users SET page = '0' "
                    f"WHERE user_id = '{user_id}';")
        else:
            with connect.cursor() as cursor:
                cursor.execute(
                    f"UPDATE users SET page = '{pg_user + pg}' "
                    f"WHERE user_id = '{user_id}';")

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT page FROM users WHERE user_id = '{user_id}'")
            pg_user = int(cursor.fetchone()[0][0])



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return pg_user

#Функция удаления карточки
def postreSQL_del_cards(name):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"DELETE FROM cards WHERE name = '{name}'")

        with connect.cursor() as cursor:
            cursor.execute(f"DELETE FROM user_cards WHERE name_card = '{name}'")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')



#Добавление пыли
def postreSQL_dust_up(user):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT attempts FROM users WHERE login = '{user['login']}'")
            dust = int(cursor.fetchone()[0][0])


        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET attempts = '{dust + int(user['attempts'])}' "
                f"WHERE login = '{user['login']}';")

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT attempts FROM users WHERE login = '{user['login']}'")



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

#Обновление вселенной
def postreSQL_universe_up(universe, user_id):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET universe = '{universe}' "
                f"WHERE user_id = '{user_id}';")


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')