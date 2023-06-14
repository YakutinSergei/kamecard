import psycopg2
from environs import Env
from lexicon.lexicon_ru import LEXICON_CARD_RARE

env = Env()
env.read_env()

def postreSQL_universe_add(name):
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )
        connect.autocommit = True

        with connect.cursor() as cursor:
            cursor.execute(f"INSERT INTO name_universes (name) "
                           f"VALUES ('{name}');")

    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')


def postgreSQL_all_universe():
    try:
        connect = psycopg2.connect(
            host=env('host'),
            user=env('user'),
            password=env('password'),
            database=env('db_name')
        )

        with connect.cursor() as cursor:
            cursor.execute(f"SELECT name FROM name_universes;")
            universe = cursor.fetchall()
            return universe



    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')