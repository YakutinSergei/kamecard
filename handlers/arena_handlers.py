import random
from datetime import datetime

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, InputMediaAnimation, InputMediaPhoto
from create_bot import bot
from data_base.arena_db import teams_db, card_user_arena, page_up_db, choice_card_db, opponent_card_db, \
    arena_attemps_up, arena_name_bd, opponent_card_name, dust_arena_up
from data_base.postreSQL_bd import user_db, postreSQL_cards_all_user_category
from keyboards.arena_kb import arena_menu_kb, arena_teams_kb, create_pag_keyboard_arena, create_inline_kb_arena

from lexicon.lexicon_ru import LEXICON_CARD, LEXICON_CARD_RARE, LEXICON_RU, LEXICON_ARENA

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


@router.callback_query(Text(startswith='card_arena_at_'))
async def choice_card(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)

    if int(callback.data.split('_')[5]) == user['id']:


        name_opp = callback.data.split('_')[3]

        opponent_card = await opponent_card_name(name_opp, user['universe'])
        # Количество атаки противника
        opp_attack = opponent_card[0]['card_1_attack'] + opponent_card[0]['card_2_attack'] + \
                     opponent_card[0]['card_3_attack'] + opponent_card[0]['card_4_attack']
        n = int(callback.data.split('_')[4])
        teams = await teams_db(callback.from_user.id, user['universe'])
        full_attack = teams['card_1_attack'] + teams['card_2_attack'] + teams['card_3_attack'] + teams[
            'card_4_attack']
        full_health = (teams['card_1_protection'] + teams['card_2_protection'] + teams['card_3_protection'] + teams[
            'card_4_protection']) - (opp_attack * (n-1))
        # Количество защиты противника
        opp_health = (opponent_card[0]['card_1_protection'] + opponent_card[0]['card_2_protection'] + \
                     opponent_card[0]['card_3_protection'] + opponent_card[0]['card_4_protection']) - (full_attack*(n-1))


        if opp_health > full_attack and full_health > opp_attack:
            await callback.message.edit_text(text=f'👊🏻🏟 Сражение между игроками \n'
                                               f'{user["login"]} 👊🏻 {name_opp}\n\n'
                                               f'Раунд {n}\n\n'
                                               f'{user["login"]}\n'
                                               f'➳ Наносит ⚔️{full_attack} урона\n'
                                               f'{name_opp}\n'
                                               f'➳ ❤️{opp_health} ➠ 💔{opp_health - full_attack}\n'
                                               f'✖️✖️✖️✖️✖️✖️\n\n'
                                               f'{name_opp}\n'
                                               f'➳ Наносит ⚔️{opp_attack} урона\n'
                                               f'{user["login"]}\n'
                                               f'➳ ❤️{full_health} ➠ 💔{full_health - opp_attack}\n',
                                          reply_markup=create_inline_kb_arena(1, f'at_{name_opp}_'
                                                                                 f'{n+1}_{user["id"]}_',
                                                                              '👊Атаковать'))  # Имя соперника_здоровье мое_здоровье соперника_атака соперника
        elif opp_health <= full_attack:
            await callback.message.edit_text(text=f'👊🏻🏟 Сражение между игроками \n'
                                               f'{user["login"]} 👊🏻 {name_opp}\n\n'
                                               f'Раунд {n}\n\n'
                                               f'{user["login"]}\n'
                                               f'➳ Наносит ⚔️{full_attack} урона\n'
                                               f'{name_opp}\n'
                                               f'➳ ❤️{opp_health} ➠ 💔0\n'
                                               f'✖️✖️✖️✖️✖️✖️\n\n'
                                               f'👏🏻Ты победил\n'
                                               f'🎁Тебе начислено 5 пыли🌸')
            await dust_arena_up(callback.from_user.id)
        else:
            await callback.message.edit_text(text=f'👊🏻🏟 Сражение между игроками \n'
                                               f'{user["login"]} 👊🏻 {name_opp}\n\n'
                                               f'Раунд {n}\n\n'
                                               f'{user["login"]}\n'
                                               f'➳ Наносит ⚔️{full_attack} урона\n'
                                               f'{name_opp}\n'
                                               f'➳ ❤️{opp_health} ➠ 💔{opp_health - full_attack}\n'
                                               f'✖️✖️✖️✖️✖️✖️\n\n'
                                               f'{name_opp}\n'
                                               f'➳ Наносит ⚔️{opp_attack} урона\n'
                                               f'➳ ❤️{full_health} ➠ 💔0\n'
                                               f'✖️✖️✖️✖️✖️✖️\n'
                                               f'Ты проиграл\n')
    await callback.answer()

@router.callback_query(Text(startswith='card_arena'))
async def choice_card(callback: CallbackQuery):
    if callback.data.split("__")[-1] ==  LEXICON_RU['back']:
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
    elif int(callback.data.split('__')[0].split('_')[-1]) == int(callback.from_user.id):
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
    user_id = int(callback.data.split('_')[2])
    if user_id == int(callback.from_user.id):
        btn_card = callback.data.split('_')[-1]
        user = await user_db(callback.from_user.id)
        pg = int(user['page'])
        category = callback.data.split('_')[-3]
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
                               reply_markup=create_inline_kb_arena(1, f'{user["id"]}__{btn}__',
                                                                   f"{LEXICON_CARD_RARE['usual']} {cards_user[0]}",
                                                                   f"{LEXICON_CARD_RARE['rare']} {cards_user[1]}",
                                                                   f"{LEXICON_CARD_RARE['epic']} {cards_user[2]}",
                                                                   f"{LEXICON_CARD_RARE['mythical']} {cards_user[3]}",
                                                                   f"{LEXICON_CARD_RARE['legendary']}  {cards_user[4]}",
                                                                   LEXICON_RU['back']))
    await callback.answer()


@router.callback_query(Text(startswith='choice_'))
async def choice_card(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    user_id = int(callback.data.split('_')[1])
    if user_id == user["id"]:
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


@router.callback_query(Text(startswith=LEXICON_ARENA['search']))
async def search_match(callback: CallbackQuery):
    if int(callback.data.split('_')[-1]) == callback.from_user.id:
        user = await user_db(callback.from_user.id)
        teams = await teams_db(callback.from_user.id, user['universe'])
        opponent_card = await opponent_card_db(callback.from_user.id, user['universe'])
        difference = datetime.now() - teams['date']
        seconds = difference.total_seconds()
        hours = seconds / (60 * 60)
        minutes = seconds / 60
        attampts = int(teams['attemps'])
        if int(hours) >= 1:
            arena_attemps_up(callback.from_user.id, 1)
            # postreSQL_attempts_user_up(message.from_user.id, 1)
            # postreSQL_data_user_up(message.from_user.id)
            attampts += 1
        if attampts <= 0:
            await callback.answer(
                text=f'Вы уже учавствовали в битве\nСледующая попытка через:  {(59 - (int(minutes) % 60))} мин.', show_alert=True)
        elif opponent_card:
            n = random.randint(0, len(opponent_card) - 1)
            name_opp = await arena_name_bd(callback.from_user.id, opponent_card[n]['user_id'])
            teams = await teams_db(callback.from_user.id, user['universe'])
            full_attack = teams['card_1_attack'] + teams['card_2_attack'] + teams['card_3_attack'] + teams[
                'card_4_attack']
            full_health = teams['card_1_protection'] + teams['card_2_protection'] + teams['card_3_protection'] + teams[
                'card_4_protection']


            #Количество атаки противника
            opp_attack = opponent_card[n]['card_1_attack'] + opponent_card[n]['card_2_attack'] +\
                         opponent_card[n]['card_3_attack'] + opponent_card[n]['card_4_attack']
            #Количество защиты противника
            opp_health = opponent_card[n]['card_1_protection'] + opponent_card[n]['card_2_protection'] + \
                         opponent_card[n]['card_3_protection'] + opponent_card[n]['card_4_protection']
            if opp_health > full_attack and full_health > opp_attack:
                await callback.message.answer(text=f'👊🏻🏟 Сражение между игроками \n'
                                                   f'{name_opp[0]} 👊🏻 {name_opp[1]}\n\n'
                                                   f'Раунд 1\n\n'
                                                   f'{name_opp[0]}\n'
                                                   f'➳ Наносит ⚔️{full_attack} урона\n'
                                                   f'{name_opp[1]}\n'
                                                   f'➳ ❤️{opp_health} ➠ 💔{opp_health - full_attack}\n'
                                                   f'✖️✖️✖️✖️✖️✖️\n\n'
                                                   f'{name_opp[1]}\n'
                                                   f'➳ Наносит ⚔️{opp_attack} урона\n\n'
                                                   f'➳ ❤️{full_health} ➠ 💔{full_health - opp_attack}\n',
                                              reply_markup=create_inline_kb_arena(1, f'at_{name_opp[1]}_2_{user["id"]}_',
                                                                                  '👊Атаковать')) #Имя соперника_здоровье мое_здоровье соперника_атака соперника
            elif opp_health <= full_attack:
                await callback.message.answer(text=f'👊🏻🏟 Сражение между игроками \n'
                                                   f'{name_opp[0]} 👊🏻 {name_opp[1]}\n\n'
                                                   f'Раунд 1\n\n'
                                                   f'{name_opp[0]}\n'
                                                   f'➳ Наносит ⚔️{full_attack} урона\n\n'
                                                   f'{name_opp[1]}\n'
                                                   f'➳ ❤️{opp_health} ➠ 💔0\n'
                                                   f'✖️✖️✖️✖️✖️✖️\n'
                                                   f'👏🏻Ты победил\n'
                                                   f'🎁Тебе начислено 5 пыли🌸')
                await dust_arena_up(callback.from_user.id)
            else:
                await callback.message.answer(text=f'👊🏻🏟 Сражение между игроками \n'
                                                   f'{name_opp[0]} 👊🏻 {name_opp[1]}\n\n'
                                                   f'Раунд 1\n\n'
                                                   f'{name_opp[0]}\n'
                                                   f'➳ Наносит ⚔️{full_attack} урона\n\n'
                                                   f'{name_opp[1]}\n'
                                                   f'➳ ❤️{opp_health} ➠ 💔{opp_health - full_attack}\n'
                                                   f'✖️✖️✖️✖️✖️✖️\n'
                                                   f'{name_opp[1]}\n'
                                                   f'➳ Наносит ⚔️{opp_attack} урона\n\n'
                                                   f'➳ ❤️{full_health} ➠ 💔0\n'
                                                   f'✖️✖️✖️✖️✖️✖️\n'
                                                   f'Ты проиграл\n')


            await arena_attemps_up(callback.from_user.id, -1)

    await callback.answer()



