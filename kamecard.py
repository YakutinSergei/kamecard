import asyncio
import logging

from aiogram.types import BotCommand

from handlers import other_handlers, user_handlers, admin_handlers, promo_handkers
from create_bot import bot, dp
from data_base import postreSQL_bd

# Инициализируем логгер
logger = logging.getLogger(__name__)

async def set_main_menu():
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/profile',
                   description='Профиль'),
        BotCommand(command='/shop',
                   description='Магазин')]

    await bot.set_my_commands(main_menu_commands)
# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    #Подключаемся к базе данных
    #postreSQL_bd.postreSQL_connect()
    await postreSQL_bd.db_connect()
    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    dp.include_router(admin_handlers.router)
    dp.include_router(promo_handkers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    dp.startup.register(set_main_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())