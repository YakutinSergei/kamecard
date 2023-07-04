import datetime

import asyncpg

from environs import Env

env = Env()
env.read_env()


#получение логина игрока
async  def comands_bd(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        commands = await conn.fetch(
            f"SELECT * FROM arena WHERE user_id ={user_id} AND ful = 1")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return commands
            print('[INFO] PostgresSQL closed')