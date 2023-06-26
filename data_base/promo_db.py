import asyncpg

from environs import Env

env = Env()
env.read_env()


async def promo_add(promo):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.execute('''INSERT INTO promo(promocode, validity, number_attempts) 
                                                        VALUES($1, $2, $3)''',
                           promo['promocode'], int(promo['validity']), int(promo['number_attempts']))
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

# Список промокодов
async def all_promo():
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        promo = await conn.fetch(f'SELECT * FROM promo WHERE validity > 0')
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return promo
            print('[INFO] PostgresSQL closed')

#Активация промокода
async def promo_user(name, user_id):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        promo = await conn.fetchrow(f"SELECT * FROM promo WHERE promocode='{name}'")

        if promo:
            if not await conn.fetchrow(f"SELECT * FROM promo_user WHERE promocode='{name}' AND user_id = {user_id}"):
                await conn.execute('''INSERT INTO promo_user(promocode, user_id) VALUES($1, $2)''', name, user_id)
                await conn.fetchrow(f"UPDATE promo SET validity = validity - 1 WHERE promocode=$1", name)
                attemps = await conn.fetchrow(f"SELECT number_attempts FROM promo WHERE promocode='{name}'")
                user_attemps = await conn.fetchrow(f"SELECT attempts FROM users WHERE user_id='{user_id}'")
                await conn.fetchrow(f"UPDATE users SET attempts = $1 WHERE user_id=$2",
                                    str(attemps['number_attempts']+ int(user_attemps['attempts'])), str(user_id))

                add = True
            else:
                add = False



    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return promo, add
            print('[INFO] PostgresSQL closed')

