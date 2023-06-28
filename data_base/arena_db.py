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

async def card_user_arena(user_id, category):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        card = await conn.fetch(f"SELECT cards.name, cards.img, cards.rare, cards.attack, cards.protection,"
                                f"cards.value, cards.universe FROM cards JOIN user_cards "
                                f"ON cards.name = name_card AND user_id='{user_id}' AND user_cards.rare = '{category}'")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            return card
            await conn.close()

            print('[INFO] PostgresSQL closed')

async def page_up_db(user_id, pg_up):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        if pg_up == -2:
            await conn.fetch(f"UPDATE users SET page = '0' WHERE user_id = '{user_id}';")
        else:
            pg = await conn.fetchrow(f"SELECT page FROM users WHERE user_id='{user_id}'")
            print(int(pg['page']))
            page = int(pg['page']) + pg_up
            print(page)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()

            print('[INFO] PostgresSQL closed')