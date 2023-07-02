import random

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from create_bot import bot
from aiogram.types import Message

from data_base.arena_db import arena_name_bd, teams_db, opponent_card_name, opponent_card_db
from data_base.postreSQL_bd import user_db
from keyboards.arena_kb import create_inline_kb_arena
from keyboards.pvp_kb import create_inline_pvp_arena
from keyboards.user_kb import create_inline_kb

router: Router = Router()

@router.message(Text(text='/пвп'))
async def pvp_challenge(message: Message):
    if message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id !=message.from_user.id:
            user = await user_db(message.from_user.id)
            teams = await teams_db(message.reply_to_message.from_user.id, user['universe'])
            print(teams['ful'])
            if teams['ful']:
                oop_name = await arena_name_bd(message.from_user.id, message.reply_to_message.from_user.id)
                await message.answer(text=f'🎪 <b>{oop_name[1]}</b>, игрок <b>{oop_name[0]}</b> бросает тебе вызов '
                                      f'и предлогает устроить дружеский матч!⚔️',
                                 reply_markup=create_inline_kb(1, f'pvp_{message.from_user.id}_{message.reply_to_message.from_user.id}_', '👊🏼Принять бой'))
            else:
                oop_name = await arena_name_bd(message.from_user.id, message.reply_to_message.from_user.id)
                await message.answer(text=f'🎪 <b>{oop_name[1]}</b>, игрок <b>{oop_name[0]}</b> бросает тебе вызов '
                                          f'и предлогает устроить дружеский матч!⚔️\n'
                                          f'_________________\n'
                                          f'К сожелению у тебя во вселенной <b><u>{user["universe"]}</u></b> не собрана команда\n'
                                          f'Собери команду или выбери ее с другой вселенной',
                                     reply_markup=create_inline_kb(1,
                                                                   f'change_🏟Арена_',
                                                                   '🔢 Собрать команду', '🪐Выбрать другую команду'))



#Выбор другой команды
@router.callback_query(Text(startswith='change_🏟Арена_🪐Выбрать другую команду'))
async def cards_universe(callback: CallbackQuery):


@router.callback_query(Text(startswith='pvp_'))
async def choice_card(callback: CallbackQuery):
    if int(callback.data.split('_')[2]) == callback.from_user.id:
        user = await user_db(callback.from_user.id)
        opponent_card = await teams_db(callback.data.split('_')[1], user['universe'])
        name_opp = await arena_name_bd(callback.from_user.id, callback.data.split('_')[1])
        teams = await teams_db(callback.from_user.id, user['universe'])
        full_attack = teams['card_1_attack'] + teams['card_2_attack'] + teams['card_3_attack'] + teams[
            'card_4_attack']
        full_health = teams['card_1_protection'] + teams['card_2_protection'] + teams['card_3_protection'] + teams[
            'card_4_protection']

        # Количество атаки противника
        opp_attack = opponent_card['card_1_attack'] + opponent_card['card_2_attack'] + \
                     opponent_card['card_3_attack'] + opponent_card['card_4_attack']
        # Количество защиты противника
        opp_health = opponent_card['card_1_protection'] + opponent_card['card_2_protection'] + \
                     opponent_card['card_3_protection'] + opponent_card['card_4_protection']
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
                                               f'➳ Наносит ⚔️{opp_attack} урона\n'
                                               f'{name_opp[0]}\n'
                                               f'➳ ❤️{full_health} ➠ 💔{full_health - opp_attack}\n',
                                          reply_markup=create_inline_pvp_arena(1, f'{name_opp[1]}_2_{user["id"]}_',
                                                                              '👊Атаковать'))  # Имя соперника_здоровье мое_здоровье соперника_атака соперника
        elif opp_health <= full_attack:
            await callback.message.answer(text=f'👊🏻🏟 Сражение между игроками \n'
                                               f'{name_opp[0]} 👊🏻 {name_opp[1]}\n\n'
                                               f'Раунд 1\n\n'
                                               f'{name_opp[0]}\n'
                                               f'➳ Наносит ⚔️{full_attack} урона\n\n'
                                               f'{name_opp[1]}\n'
                                               f'➳ ❤️{opp_health} ➠ 💔0\n'
                                               f'✖️✖️✖️✖️✖️✖️\n'
                                               f'👏🏻Ты победил\n')
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

    await callback.answer()


@router.callback_query(Text(startswith='pvparena_'))
async def choice_card(callback: CallbackQuery):
    user = await user_db(callback.from_user.id)
    print(callback.data)

    if int(callback.data.split('_')[3]) == user['id']:


        name_opp = callback.data.split('_')[1]

        opponent_card = await opponent_card_name(name_opp, user['universe'])
        print(opponent_card)
        # Количество атаки противника
        opp_attack = opponent_card[0]['card_1_attack'] + opponent_card[0]['card_2_attack'] + \
                     opponent_card[0]['card_3_attack'] + opponent_card[0]['card_4_attack']
        n = int(callback.data.split('_')[2])
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
                                          reply_markup=create_inline_pvp_arena(1, f'{name_opp}_'
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
                                               f'👏🏻Ты победил\n')
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