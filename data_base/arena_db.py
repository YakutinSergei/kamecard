import datetime

import asyncpg

from environs import Env

env = Env()
env.read_env()


async def teams_db(user_id, universe: str):
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
                                                    $3, 1, 0)''', int(user_id), universe, datetime.datetime.now())
            user = await conn.fetchrow(f"SELECT * FROM arena WHERE user_id='{user_id}' AND universe = '{universe}'")
        return user

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()

            print('[INFO] PostgresSQL closed')


#Получение карт юзера которые могут учавствовать на арене

async def card_user_arena(user_id, category,universe):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        card = await conn.fetch(f"SELECT cards.name, cards.img, cards.rare, cards.attack, cards.protection,"
                                f"cards.value, cards.universe FROM cards JOIN user_cards "
                                f"ON cards.name = name_card AND user_id='{user_id}' AND user_cards.rare = '{category}'"
                                f"AND cards.universe = '{universe}'")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            return card
            await conn.close()

            print('[INFO] PostgresSQL closed')

#Обновление страницы
async def page_up_db(user_id, pg_up):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        if pg_up == -2:
            await conn.fetch(f"UPDATE users SET page = '0' WHERE user_id = '{user_id}';")
        else:
            pg = await conn.fetchrow(f"SELECT page FROM users WHERE user_id='{user_id}'")
            page = int(pg['page']) + pg_up
            await conn.fetch(f"UPDATE users SET page = '{page}' WHERE user_id = '{user_id}';")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()

            print('[INFO] PostgresSQL closed')


async def choice_card_db(user_id, name_card, num_card):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))


        await conn.fetch(f"UPDATE users SET page = '0' WHERE user_id = '{user_id}';")

        card = await conn.fetchrow(f"SELECT * FROM cards WHERE name='{name_card}'")

        await conn.fetch(f"UPDATE arena SET card_{num_card}_name = '{card['name']}', "
                                            f"card_{num_card}_attack = '{card['attack']}', "
                                            f"card_{num_card}_protection = '{card['protection']}' "
                                            f"WHERE user_id = '{user_id}' AND universe = '{card['universe']}';")

        user = await conn.fetchrow(f"SELECT * FROM arena WHERE user_id='{user_id}' AND universe = '{card['universe']}'")

        if not user['card_1_name'] == 'Пусто' and not user['card_2_name'] == 'Пусто' and not user['card_3_name'] == 'Пусто' and not user['card_4_name'] == 'Пусто':
            await conn.fetch(f"UPDATE arena SET ful = '1' "
                             f"WHERE user_id = '{user_id}' AND universe = '{card['universe']}';")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')


#Поиск карт противника
async def opponent_card_db(user_id, universe):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        opponent_card = await conn.fetch(f"SELECT * FROM arena WHERE user_id !='{user_id}' AND universe = '{universe}'"
                                         f" AND ful = '1'")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return opponent_card
            print('[INFO] PostgresSQL closed')

# Обнвовление попыток арены
async def arena_attemps_up(user_id, attemps):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        await conn.fetch(f"UPDATE arena SET attemps = attemps + {attemps}, date = '{datetime.datetime.now()}' WHERE user_id = '{user_id}'")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

#Получение имени игрока
async def arena_name_bd(user_id, user_opp):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        name_user = await conn.fetchrow(f"SELECT login FROM users WHERE user_id ='{user_id}'")
        name_opp = await conn.fetchrow(f"SELECT login FROM users WHERE user_id ='{user_opp}'")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return name_user['login'], name_opp['login']
            print('[INFO] PostgresSQL closed')


# Имя карточки
async def opponent_card_name(name, universe):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))

        user_id = await conn.fetchrow(f"SELECT user_id FROM users WHERE login ='{name}'")
        opponent_card = await conn.fetchrow(f"SELECT * FROM arena WHERE user_id = '{user_id['user_id']}' AND universe = '{universe}'")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return opponent_card
            print('[INFO] PostgresSQL closed')


async def dust_arena_up(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        sum_dust = await conn.fetchrow(f"SELECT sum_dust FROM users WHERE user_id ='{user_id}'")

        await conn.fetch(f"UPDATE users SET sum_dust = '{int(sum_dust['sum_dust']) + 15}'"
                         f"WHERE user_id = '{user_id}';")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')



async def all_users_statistics(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        i_users = None
        users = await conn.fetch(f"SELECT *FROM users ORDER BY points DESC")
        for i in range(len(users)):
            if user_id == users[i]['user_id']:
                i_users = i+1

        users = await conn.fetch(f"SELECT *FROM users ORDER BY points DESC LIMIT 10")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return users, i_users
            print('[INFO] PostgresSQL closed')


#Все пользователи для рассылки
async def all_users():
    try:
        conn = await asyncpg.connect(user=env('user'), password=env('password'), database=env('db_name'),
                                     host=env('host'))
        users = await conn.fetch(f"SELECT user_id FROM users")

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return users
            print('[INFO] PostgresSQL closed')