import datetime

import asyncpg

from environs import Env

env = Env()
env.read_env()


#получение логина игрока
