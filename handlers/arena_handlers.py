from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InputMediaAnimation, InputMediaPhoto
from create_bot import bot
from data_base.arena_db import teams_db, card_user_arena, page_up_db, choice_card_db
from data_base.postreSQL_bd import postreSQL_users, user_db, postreSQL_cards_all_category, \
    postreSQL_cards_all_user_category
from data_base.promo_db import promo_add, all_promo, promo_user
from keyboards.admin_kb import create_inline_kb
from keyboards.arena_kb import arena_menu_kb, arena_teams_kb, create_pag_keyboard_arena, create_inline_kb_arena

from lexicon.lexicon_ru import LEXICON_CARD, LEXICON_PROMO, LEXICON_CARD_RARE, LEXICON_RU, LEXICON_ARENA

router: Router = Router()



@router.callback_query(Text(startswith='change_🏟Арена'))
async def process_name_card(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    teams = await teams_db(callback.from_user.id, user['universe'])
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

@router.callback_query(Text(startswith=LEXICON_ARENA['teams']))
async def teams_user(callback: CallbackQuery):
    if int(callback.data.split('_')[-1]) == callback.from_user.id:
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
    if int(callback.data.split('__')[-1]) == callback.from_user.id:
        user = await user_db(callback.from_user.id)
        cards_user = postreSQL_cards_all_user_category(callback.from_user.id, user['universe'])
        btn: str = callback.data.split('__')[0].split('_')[-1]
        await bot.send_message(chat_id=callback.message.chat.id, text=f'❗️Карты игрока {user[2]}',
                               reply_markup=create_inline_kb_arena(1, f'{callback.from_user.id}__{btn}__',
                                                             f"{LEXICON_CARD_RARE['usual']} {cards_user[0]}",
                                                             f"{LEXICON_CARD_RARE['rare']} {cards_user[1]}",
                                                             f"{LEXICON_CARD_RARE['epic']} {cards_user[2]}",
                                                             f"{LEXICON_CARD_RARE['mythical']} {cards_user[3]}",
                                                             f"{LEXICON_CARD_RARE['legendary']}  {cards_user[4]}",
                                                             LEXICON_RU['back']))
    await callback.answer()

@router.callback_query(Text(startswith='card_arena'))
async def choice_card(callback: CallbackQuery):
    print(callback.data)
    if int(callback.data.split('__')[0].split('_')[-1]) == int(callback.from_user.id):
        btn_card = callback.data.split('__')[1].split('_')[-1]
        await page_up_db(callback.from_user.id, -2)
        user = await user_db(callback.from_user.id)
        pg = int(user['page'])
        category = callback.data.split('__')[-1].split(' ')[0]
        cards = await card_user_arena(user['user_id'], category)
        if len(cards) > 0:
            if cards[pg]['img'].split('__')[0] == 'gif':
                await bot.send_animation(chat_id=callback.message.chat.id, animation=cards[pg]['img'][5:],
                                                                        caption=f'{cards[pg]["name"]}\n'
                                                                                f'{LEXICON_CARD["rere"]} {cards[pg]["rare"][1:]}\n'
                                                                                f'{LEXICON_CARD["attack"]} {cards[pg]["attack"]}\n'
                                                                                f'{LEXICON_CARD["health"]} {cards[pg]["protection"]}\n\n'
                                                                                f'{LEXICON_CARD["value"]} {cards[pg]["value"]} kms\n\n'
                                                                                f'_______________________________\n'
                                                                                f'❗️Карты игрока {user["login"]}',
                                                                        reply_markup=create_pag_keyboard_arena(callback.from_user.id,
                                                                                                               category+f'_{cards[pg]["name"]}_{btn_card}',
                                                                                                               'backward',
                                                                                                                f'{pg + 1}/{len(cards)}',
                                                                                           'forward'))
                await callback.answer()
            else:
                await bot.send_photo(chat_id=callback.message.chat.id,
                                                photo=cards[pg]['img'][7:],
                                                caption=f'{cards[pg]["name"]}\n'
                                                         f'{LEXICON_CARD["rere"]} {cards[pg]["rare"][1:]}\n'
                                                         f'{LEXICON_CARD["attack"]} {cards[pg]["attack"]}\n'
                                                         f'{LEXICON_CARD["health"]} {cards[pg]["protection"]}\n\n'
                                                         f'{LEXICON_CARD["value"]} {cards[pg]["value"]} kms\n\n'
                                                         f'_______________________________\n'
                                                         f'❗️Карты игрока {user["login"]}',
                                                reply_markup=create_pag_keyboard_arena(callback.from_user.id, category+f'_{cards[pg]["name"]}_{btn_card}',
                                                                                     'backward',
                                                                                           f'{pg + 1}/{len(cards)}',
                                                                                           'forward'))
    await callback.answer()


# Кнопка вперед
@router.callback_query(Text(startswith='ar_forward_'))
async def process_forward_press(callback: CallbackQuery):
    print(callback.data)
    user_id = int(callback.data.split('_')[2])
    if user_id == int(callback.from_user.id):
        btn_card = callback.data.split('_')[-1]
        user = await user_db(callback.from_user.id)
        pg = int(user['page'])
        category = callback.data.split('_')[-3]
        print(callback.data)
        print(category)
        cards = await card_user_arena(user['user_id'], category)
        if len(cards) > (pg + 1):
            await page_up_db(callback.from_user.id, 1)
            pg += 1
            if cards[pg]['img'].split('__')[0] == 'gif':
                await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                             media=InputMediaAnimation(media=cards[pg]['img'][5:],
                                                                        caption=f'{cards[pg]["name"]}\n'
                                                                                f'{LEXICON_CARD["rere"]} {cards[pg]["rare"][1:]}\n'
                                                                                f'{LEXICON_CARD["attack"]} {cards[pg]["attack"]}\n'
                                                                                f'{LEXICON_CARD["health"]} {cards[pg]["protection"]}\n\n'
                                                                                f'{LEXICON_CARD["value"]} {cards[pg]["value"]} kms\n\n'
                                                                                f'_______________________________\n'
                                                                                f'❗️Карты игрока {user["login"]}'),
                                                                        reply_markup=create_pag_keyboard_arena(callback.from_user.id,
                                                                                                               category+f'_{cards[pg]["name"]}_{btn_card}',
                                                                                                               'backward',
                                                                                                                f'{pg + 1}/{len(cards)}',
                                                                                           'forward'))
            else:
                await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                             media=InputMediaPhoto(media=cards[pg]['img'][7:],
                                                caption=f'{cards[pg]["name"]}\n'
                                                         f'{LEXICON_CARD["rere"]} {cards[pg]["rare"][1:]}\n'
                                                         f'{LEXICON_CARD["attack"]} {cards[pg]["attack"]}\n'
                                                         f'{LEXICON_CARD["health"]} {cards[pg]["protection"]}\n\n'
                                                         f'{LEXICON_CARD["value"]} {cards[pg]["value"]} kms\n\n'
                                                         f'_______________________________\n'
                                                         f'❗️Карты игрока {user["login"]}'),
                                                        reply_markup=create_pag_keyboard_arena(callback.from_user.id, category+f'_{cards[pg]["name"]}_{btn_card}',
                                                                                               'backward',
                                                                                                   f'{pg + 1}/{len(cards)}',
                                                                                                   'forward'))
    await callback.answer()

@router.callback_query(Text(startswith='ar_backward_'))
async def process_forward_press(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[2])
    if user_id == int(callback.from_user.id):
        btn_card = callback.data.split('_')[-1]
        user = await user_db(callback.from_user.id)
        pg = int(user['page'])
        category = callback.data.split('_')[-3]
        cards = await card_user_arena(user['user_id'], category)
        if pg > 0:

            await page_up_db(callback.from_user.id, -1)
            pg -= 1
            if cards[pg]['img'].split('__')[0] == 'gif':
                await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                             media=InputMediaAnimation(media=cards[pg]['img'][5:],
                                                                        caption=f'{cards[pg]["name"]}\n'
                                                                                f'{LEXICON_CARD["rere"]} {cards[pg]["rare"][1:]}\n'
                                                                                f'{LEXICON_CARD["attack"]} {cards[pg]["attack"]}\n'
                                                                                f'{LEXICON_CARD["health"]} {cards[pg]["protection"]}\n\n'
                                                                                f'{LEXICON_CARD["value"]} {cards[pg]["value"]} kms\n\n'
                                                                                f'_______________________________\n'
                                                                                f'❗️Карты игрока {user["login"]}'),
                                                                        reply_markup=create_pag_keyboard_arena(callback.from_user.id, category+f'_{cards[pg]["name"]}_{btn_card}',
                                                                                                                'backward',
                                                                                                                f'{pg + 1}/{len(cards)}',
                                                                                                                'forward'))
                await callback.answer()
            else:
                await bot.edit_message_media(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                             media=InputMediaPhoto(media=cards[pg]['img'][7:],
                                                caption=f'{cards[pg]["name"]}\n'
                                                         f'{LEXICON_CARD["rere"]} {cards[pg]["rare"][1:]}\n'
                                                         f'{LEXICON_CARD["attack"]} {cards[pg]["attack"]}\n'
                                                         f'{LEXICON_CARD["health"]} {cards[pg]["protection"]}\n\n'
                                                         f'{LEXICON_CARD["value"]} {cards[pg]["value"]} kms\n\n'
                                                         f'_______________________________\n'
                                                         f'❗️Карты игрока {user["login"]}'),
                                                reply_markup=create_pag_keyboard_arena(callback.from_user.id, category+f'_{cards[pg]["name"]}_{btn_card}',
                                                                                        'backward',
                                                                                        f'{pg + 1}/{len(cards)}',
                                                                                        'forward'))
    await callback.answer()


@router.callback_query(Text(startswith='back_Card_'))
async def back_category_command(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[2])
    if user_id == callback.from_user.id:
        user = await user_db(callback.from_user.id)
        cards_user = postreSQL_cards_all_user_category(callback.from_user.id, user['universe'])
        btn: str = callback.data.split('_')[-1]
        await bot.send_message(chat_id=callback.message.chat.id, text=f'❗️Карты игрока {user[2]}',
                               reply_markup=create_inline_kb_arena(1, f'{callback.from_user.id}__{btn}__',
                                                                   f"{LEXICON_CARD_RARE['usual']} {cards_user[0]}",
                                                                   f"{LEXICON_CARD_RARE['rare']} {cards_user[1]}",
                                                                   f"{LEXICON_CARD_RARE['epic']} {cards_user[2]}",
                                                                   f"{LEXICON_CARD_RARE['mythical']} {cards_user[3]}",
                                                                   f"{LEXICON_CARD_RARE['legendary']}  {cards_user[4]}",
                                                                   LEXICON_RU['back']))
    await callback.answer()


@router.callback_query(Text(startswith='choice_'))
async def choice_card(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[1])
    print(callback.data)
    if user_id == callback.from_user.id:
        user = await user_db(callback.from_user.id)
        teams = await teams_db(callback.from_user.id, user['universe'])
        cards = [f'{teams["card_1_name"]}', f'{teams["card_2_name"]}', f'{teams["card_3_name"]}', f'{teams["card_4_name"]}']
        card = callback.data.split('_')[-2]
        if card in cards:
            await callback.answer(text="Эта карта уже у вас в команде")
        else:
            await choice_card_db(callback.from_user.id, card, callback.data.split('_')[-1])
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
    await callback.answer()


@router.callback_query(Text(startswith='back_arena_'))
async def back_arena_command(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    teams = await teams_db(callback.from_user.id, user['universe'])
    full_attack = teams['card_1_attack'] + teams['card_2_attack'] + teams['card_3_attack'] + teams['card_4_attack']
    full_health = teams['card_1_protection'] + teams['card_2_protection'] + teams['card_3_protection'] + teams[
        'card_4_protection']
    await callback.message.answer(
        text=f'🏟 {user[2]}, ты можешь собрать команду из карт и сражаться с другими игроками\n\n'
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
