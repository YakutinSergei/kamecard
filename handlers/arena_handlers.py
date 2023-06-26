from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from create_bot import bot
from data_base.arena_db import teams_db
from data_base.postreSQL_bd import postreSQL_users
from data_base.promo_db import promo_add, all_promo, promo_user
from keyboards.admin_kb import create_inline_kb

from lexicon.lexicon_ru import LEXICON_CARD, LEXICON_PROMO, LEXICON_CARD_RARE, LEXICON_RU

router: Router = Router()


@router.message(Text(text=['меню', 'Меню', 'МЕНЮ']))
async def process_name_card(message: Message, state: FSMContext):
    user = postreSQL_users(message.from_user.id)
    teams = teams_db(message.from_user.id, user[3])
    await message.answer(text=f'🏟 {user[2]}, ты можешь собрать команду из карт и сражаться с другими игроками\n\n'
                              f'🔢<b>Твоя команда</b>\n'
                              f'1️⃣ \n'
                              f'2️⃣ \n'
                              f'3️⃣ \n'
                              f'4️⃣ \n'
                              f'_________________\n'
                              f'⚔️Атака: \n'
                              f'❤️Здоровье: \n')