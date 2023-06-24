from datetime import datetime
import asyncpg

import psycopg2
from environs import Env
from lexicon.lexicon_ru import LEXICON_CARD_RARE

env = Env()
env.read_env()

# Функция подключения к базе


async def db_connect():
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.execute('''CREATE TABLE IF NOT EXISTS users(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                user_id INTEGER NOT NULL,
                                                               login VARCHAR(50) NOT NULL,
                                                               universe VARCHAR(50) NOT NULL,             
                                                               sum_dust VARCHAR(50) NOT NULL,            
                                                               attempts VARCHAR(50) NOT NULL,  
                                                               status VARCHAR(10) NOT NULL, 
                                                               page VARCHAR(50),
                                                               chance_epic VARCHAR(10),
                                                               chance_mythical VARCHAR(10),
                                                               chance_legendary VARCHAR(10),
                                                               data VARCHAR(50) NOT NULL,
                                                               points VARCHAR(50) NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS cards(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                               name VARCHAR(50) NOT NULL,
                                                               img VARCHAR(100) NOT NULL,   
                                                               rare VARCHAR(50) NOT NULL,            
                                                               attack VARCHAR(50) NOT NULL,          
                                                               protection VARCHAR(50) NOT NULL,      
                                                               value VARCHAR(50) NOT NULL,           
                                                               universe VARCHAR(50) NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS user_cards(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                    user_id VARCHAR(50) NOT NULL,
                                                                    rare VARCHAR(50) NOT NULL,
                                                                    name_card VARCHAR(100) NOT NULL,
                                                                    universe VARCHAR(100) NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS name_universes (id BIGSERIAL NOT NULL PRIMARY KEY,
                           name VARCHAR(50) NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS promo(id BIGSERIAL NOT NULL PRIMARY KEY, 
                                                                promocode VARCHAR(50) NOT NULL,
                                                                validity INTEGER NOT NULL, 
                                                                number_attempts INTEGER NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS promo_user(id BIGSERIAL NOT NULL PRIMARY KEY, 
                                                                promocode VARCHAR(50) NOT NULL,
                                                                user_id INTEGER NOT NULL);''')

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
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
            cursor.execute(f"INSERT INTO users (user_id, login, status, universe, sum_dust, attempts, page, chance_epic, chance_mythical, chance_legendary, data, points) "
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
                           f"'{datetime.now()}',"
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
            cursor.execute(f"INSERT INTO cards (name, img, rare, attack, protection, value, universe) VALUES ('{card['neme']}',"
                                                                                                    f"'{card['img']}',"
                                                                                                    f"'{card['rare']}',"
                                                                                                    f"'{card['attack']}',"
                                                                                                    f"'{card['protection']}',"
                                                                                                    f"'{value_card}',"
                                                                                                    f"'{card['universe']}');")



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


#Все карты для категории и вселенной
def postreSQL_cards(category, universe):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{category}' AND universe = '{universe}';")
            cards = cursor.fetchall()
            return cards

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


#Показ карточек админа
def postreSQL_cards_admin(category):
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
# функция обновления страницы
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
            pg_user = int(cursor.fetchone()[0])

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
            pg_user = int(cursor.fetchone()[0])


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



#Добавление попыток
def postreSQL_attempts_up(user):
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
            attempts = int(cursor.fetchone()[0])


        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET attempts = '{attempts + int(user['attempts'])}' "
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


#Добавление карт
def postgreSQL_add_card_user(user_id, name_card, rare, universe):  #rare - категория
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        value_card = 0
        if rare == LEXICON_CARD_RARE['usual']:
            value_card = 500
        elif rare == LEXICON_CARD_RARE['rare']:
            value_card = 1500
        elif rare == LEXICON_CARD_RARE['epic']:
            value_card = 6000
        elif rare == LEXICON_CARD_RARE['mythical']:
            value_card = 12000
        elif rare == LEXICON_CARD_RARE['legendary']:
            value_card = 30000



        # Проверяем есть ли такая карта у юзера
        with connect.cursor() as cursor:
            cursor.execute(f"SELECT * FROM user_cards WHERE user_id = '{user_id}' AND name_card = '{name_card}'")
            cards = cursor.fetchone()

        #Если нет то дабовляем
        if not cards:
            with connect.cursor() as cursor:
                cursor.execute(f"INSERT INTO user_cards (user_id, rare, name_card, universe) VALUES ('{user_id}',"
                               f"'{rare}',"
                               f"'{name_card}',"
                               f"'{universe}');")

            #Возвращаем все карты юзера с новой картой
            with connect.cursor() as cursor:
                cursor.execute(f"SELECT * FROM user_cards WHERE user_id = '{user_id}' AND name_card = '{name_card}'")
                cards = cursor.fetchone()

            with connect.cursor() as cursor:
                cursor.execute(f"SELECT points FROM users WHERE user_id = '{user_id}'")
                point_user = int(cursor.fetchone()[0])

            with connect.cursor() as cursor:
                cursor.execute(
                    f"UPDATE users SET points = '{point_user + value_card}' "
                    f"WHERE user_id = '{user_id}';")
        else:
            cards = None
        return cards

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

#Получение одной карыт
def postgreSQL_cards_one(name_card):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT * FROM cards WHERE name = '{name_card}'")
            cards = cursor.fetchone()

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return cards

#Обновление пыли
def postgereSQL_dust_up(user_id, size):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT sum_dust FROM users WHERE user_id = '{user_id}'")
            dust =int(cursor.fetchone()[0])
            with connect.cursor() as cursor:
                cursor.execute(f"SELECT chance_epic, chance_mythical, chance_legendary FROM users WHERE user_id = '{user_id}'")
                size_chance = cursor.fetchone()


        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET sum_dust = '{dust + size}' "
                f"WHERE user_id = '{user_id}';")

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT sum_dust FROM users WHERE user_id = '{user_id}'")

        # #Обновление шанса
        # if name_categ == LEXICON_CARD_RARE['legendary']:
        #     with connect.cursor() as cursor:
        #         cursor.execute(
        #             f"UPDATE users SET chance_legendary = '10',  chance_epic = '{int(size_chance[0])+2}', "
        #             f"chance_mythical = '{int(size_chance[1])+2}' "
        #             f"WHERE user_id = '{user_id}';")
        #
        # elif name_categ == LEXICON_CARD_RARE['mythical']:
        #     with connect.cursor() as cursor:
        #         cursor.execute(
        #             f"UPDATE users SET chance_mythical = '30', chance_epic = '{int(size_chance[0])+2}', "
        #             f"chance_legendary = '{int(size_chance[2])+0.2}' "
        #             f"WHERE user_id = '{user_id}';")
        #
        # elif name_categ == LEXICON_CARD_RARE['epic']:
        #     with connect.cursor() as cursor:
        #         cursor.execute(
        #             f"UPDATE users SET chance_epic = '60',  chance_mythical = '{int(size_chance[1]) + 2}', "
        #             f" chance_legendary = '{int(size_chance[2]) + 2}' "
        #             f"WHERE user_id = '{user_id}';")
        # else:
        #     with connect.cursor() as cursor:
        #         cursor.execute(
        #             f"UPDATE users SET chance_epic = '{int(size_chance[0]) + 2}', chance_mythical = '{int(size_chance[1]) + 2}', "
        #             f"chance_legendary = '{int(size_chance[2]) + 2}' "
        #             f"WHERE user_id = '{user_id}';")



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

#Обновление пыпоток при получении карты и покупки попыток
def postreSQL_attempts_user_up(user_id, size):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT attempts FROM users WHERE user_id = '{user_id}'")
            attempts = int(cursor.fetchone()[0])


        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET attempts = '{attempts + size}' "
                f"WHERE user_id = '{user_id}';")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


#Функция обновление даты
def postreSQL_data_user_up(user_id):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET data = '{datetime.now()}' "
                f"WHERE user_id = '{user_id}';")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


#получение всех карт
def postreSQL_cards_all_category(universe):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{LEXICON_CARD_RARE['legendary']}' AND universe = '{universe}';")
            all_cards_legendary = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{LEXICON_CARD_RARE['mythical']}' AND universe = '{universe}';")
            all_cards_mythical = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{LEXICON_CARD_RARE['epic']}' AND universe = '{universe}';")
            all_cards_epic = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{LEXICON_CARD_RARE['rare']}' AND universe = '{universe}';")
            all_cards_rare = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM cards WHERE  rare = '{LEXICON_CARD_RARE['usual']}' AND universe = '{universe}';")
            all_cards_usual = len(cursor.fetchall())




    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return all_cards_usual, all_cards_rare, all_cards_epic, all_cards_mythical, all_cards_legendary

#Получение карт юзера
def postreSQL_cards_all_user_category(user_id, universe):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            print(universe)
            cursor.execute(f"SELECT *FROM user_cards WHERE  rare = '{LEXICON_CARD_RARE['legendary']}' AND user_id = '{user_id}' AND universe = '{universe}';")
            all_cards_legendary = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM user_cards WHERE  rare = '{LEXICON_CARD_RARE['mythical']}' AND user_id = '{user_id}' AND universe = '{universe}';")
            all_cards_mythical = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM user_cards WHERE  rare = '{LEXICON_CARD_RARE['epic']}' AND user_id = '{user_id}' AND universe = '{universe}';")
            all_cards_epic = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM user_cards WHERE  rare = '{LEXICON_CARD_RARE['rare']}' AND user_id = '{user_id}' AND universe = '{universe}';")
            all_cards_rare = len(cursor.fetchall())

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT *FROM user_cards WHERE  rare = '{LEXICON_CARD_RARE['usual']}' AND user_id = '{user_id}' AND universe = '{universe}';")
            all_cards_usual = len(cursor.fetchall())




    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return all_cards_usual, all_cards_rare, all_cards_epic, all_cards_mythical, all_cards_legendary

#Все карты пользователя
def postreSQL_cards_all_user(user_id):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        all_cards = []
        with connect.cursor() as cursor:
            cursor.execute(f"SELECT name_card FROM user_cards WHERE user_id = '{user_id}';")
            cards = cursor.fetchall()
            for i in range(len(cards)):
                all_cards.append(cards[i][0])


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return all_cards

#Получение очков юзеров
def postreSQL_point_all_user():
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        all_points = []
        with connect.cursor() as cursor:
            cursor.execute(f"SELECT points FROM users;")
            points = cursor.fetchall()
            for i in range(len(points)):
                all_points.append(int(points[i][0]))


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')
            return all_points




def postgereSQL_dust_shop(user_id, size):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT sum_dust FROM users WHERE user_id = '{user_id}'")
            dust =int(cursor.fetchone()[0])


        with connect.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET sum_dust = '{dust + size}' "
                f"WHERE user_id = '{user_id}';")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


def postreSQL_del_universe(universe):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True
        print(universe)
        with connect.cursor() as cursor:
            cursor.execute(f"DELETE FROM cards WHERE universe = '{universe}'")

        with connect.cursor() as cursor:
            cursor.execute(f"DELETE FROM user_cards WHERE universe = '{universe}'")

        with connect.cursor() as cursor:
            cursor.execute(f"DELETE FROM name_universes WHERE name = '{universe}'")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')