import datetime

import asyncpg

from environs import Env

env = Env()
env.read_env()


async def teams_db(user_id: int, universe: str):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        user = await conn.fetchrow(f"SELECT * FROM arena WHERE user_id='{user_id}' AND universe = '{universe}'")
        if not user:
            await conn.execute('''INSERT INTO arena(user_id, universe, 
                                                    card_1_name, card_1_attack, card_1_protection,
                                                    card_2_name, card_2_attack, card_2_protection,
                                                    card_3_name, card_3_attack, card_3_protection,
                                                    card_4_name, card_4_attack, card_4_protection,
                                                    date, attemps, ful) 
                                                    VALUES($1, $2, 
                                                    'Пусто', 0,0,
                                                    'Пусто', 0,0,
                                                    'Пусто', 0,0,
                                                    'Пусто', 0,0,
                                                    $3, 1, 0)''', user_id, universe, datetime.datetime.now())
            user = await conn.fetchrow(f"SELECT * FROM arena WHERE user_id='{user_id}' AND universe = '{universe}'")
        return user

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()

            print('[INFO] PostgresSQL closed')


#Получение карт юзера которые могут учавствовать на арене
async def arena_cards_user(user_id: int, universe: str, rare: str):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        user_card = await conn.fetchrow(f"SELECT * FROM user_cards WHERE rare = '{rare}' AND user_id='{user_id}' AND universe = '{universe}'")
        card_all = await conn.fetchrow(f"SELECT name FROM cards WHERE rare = '{rare}' AND universe = '{universe}'")

        card = []
        for i in range(len(user_card)):
            if user_card['name_card'] in card_all:
                print(ne)
        return user

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()

            print('[INFO] PostgresSQL closed')