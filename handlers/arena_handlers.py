from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from create_bot import bot
from data_base.arena_db import teams_db
from data_base.postreSQL_bd import postreSQL_users, user_db, postreSQL_cards_all_category, \
    postreSQL_cards_all_user_category
from data_base.promo_db import promo_add, all_promo, promo_user
from keyboards.admin_kb import create_inline_kb
from keyboards.arena_kb import arena_menu_kb, arena_teams_kb

from lexicon.lexicon_ru import LEXICON_CARD, LEXICON_PROMO, LEXICON_CARD_RARE, LEXICON_RU, LEXICON_ARENA

router: Router = Router()



@router.callback_query(Text(startswith='change_🏟Арена'))
async def process_name_card(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    teams = await teams_db(callback.from_user.id, user['universe'])
    print(teams)
    full_attack = teams['card_1_attack']+teams['card_2_attack']+teams['card_3_attack']+teams['card_4_attack']
    full_health = teams['card_1_protection']+teams['card_2_protection']+teams['card_3_protection']+teams['card_4_protection']
    await callback.message.answer(text=f'🏟 {user[2]}, ты можешь собрать команду из карт и сражаться с другими игроками\n\n'
                              f'🔢<b>Твоя команда</b>\n'
                              f'1️⃣ {teams["card_1_name"]}\n'
                              f'2️⃣ {teams["card_2_name"]}\n'
                              f'3️⃣ {teams["card_3_name"]}\n'
                              f'4️⃣ {teams["card_4_name"]}\n'
                              f'_________________\n'
                              f'⚔️Атака: {full_attack}\n'  
                              f'❤️Здоровье: {full_health}\n',
                         reply_markup=arena_menu_kb(teams))
    await callback.answer()

@router.callback_query(Text(text=LEXICON_ARENA['teams']))
async def teams_user(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    teams = await teams_db(callback.from_user.id, user['universe'])
    await callback.message.answer(
        text=f'🏟 {user[2]}, ты можешь собрать команду из карт и сражаться с другими игроками\n'
             f'➖➖➖➖➖➖➖➖➖➖\n'
             f'🔢<b>Твоя команда</b>\n'
             f'1️⃣ {teams["card_1_name"]}\n'
             f'2️⃣ {teams["card_2_name"]}\n'
             f'3️⃣ {teams["card_3_name"]}\n'
             f'4️⃣ {teams["card_4_name"]}\n',
        reply_markup=arena_teams_kb(teams))
    await callback.answer()


@router.callback_query(Text(startswith='btn_card_'))
async def card_add(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    all_cards = postreSQL_cards_all_category(user['universe'])
    cards_user = postreSQL_cards_all_user_category(callback.from_user.id, user['universe'])
    await bot.send_message(chat_id=callback.message.chat.id, text=f'❗️Карты игрока {user[2]}',
                           reply_markup=create_inline_kb(1, f'card__{callback.data}__{callback.from_user.id}_',
                                                         f"{LEXICON_CARD_RARE['usual']} {cards_user[0]}/{all_cards[0]}",
                                                         f"{LEXICON_CARD_RARE['rare']} {cards_user[1]}/{all_cards[1]}",
                                                         f"{LEXICON_CARD_RARE['epic']} {cards_user[2]}/{all_cards[2]}",
                                                         f"{LEXICON_CARD_RARE['mythical']} {cards_user[3]}/{all_cards[3]}",
                                                         f"{LEXICON_CARD_RARE['legendary']}  {cards_user[4]}/{all_cards[4]}",
                                                         LEXICON_RU['back']))

@router.callback_query(Text(startswith='card_'))
async def choice_card(callback: CallbackQuery):
    print(callback.data.split('__')[1])
    user = await user_db(callback.from_user.id)
    category = callback.data.split('__')[-1].split(' ')[0].split('_')[1]

    cards = card_user_arena(user['user_id'],user['universe'], category, callback.data.split('__')[1])
    await callback.answer()