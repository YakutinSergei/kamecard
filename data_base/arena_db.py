import asyncpg

from environs import Env

env = Env()
env.read_env()


async def teams_db(user_id, universe):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        teams = await conn.fetchrow(f"SELECT * FROM arena WHERE user_id='{user_id}' AND universe = {universe}")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return teams
            print('[INFO] PostgresSQL closed')