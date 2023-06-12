import psycopg2
from environs import Env

env = Env()
env.read_env()


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
                           "user_id VARCHAR(20) NOT NULL,"
                           "login VARCHAR(50) NOT NULL,"
                           "universe VARCHAR(50) NOT NULL,"
                           "")


    except psycopg2.Error as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if connect:
            connect.close()
            print('[INFO] PostgresSQL closed')

