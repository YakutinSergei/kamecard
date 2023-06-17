from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAnimation

from data_base.postgreSQL_bd_universal import postgreSQL_all_universe
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_CARD_RARE, LEXICON_SHOP, LEXICON_CARD
from data_base.postreSQL_bd import postreSQL_users, postreSQL_login, postreSQL_user_add, postreSQL_universe_up, \
    postreSQL_cards, postgreSQL_add_card_user, postgreSQL_cards_one, postgereSQL_dust_up, postreSQL_attempts_user_up, \
    postreSQL_data_user_up, postreSQL_cards_all_category, postreSQL_cards_all_user_category, postreSQL_pg_up, \
    postreSQL_cards_all_user, postreSQL_point_all_user, postgereSQL_dust_shop
from keyboards.user_kb import create_inline_kb, universe_kb, create_inline_kb_universe_user, menu_user, \
    create_pagination_keyboard
import random

from create_bot import bot


router: Router = Router()



class FSMorder(StatesGroup):
    name = State()

class FSMshop_dust(StatesGroup):
    count = State()

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/start'])
    await state.set_state(FSMorder.name)

@router.callback_query(Text(text='dust_shop_Отмена'), ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery):
    user = postreSQL_users(callback.from_user.id)
    dust = user[4]
    await callback.message.answer(text='Вы отменили покупку')
    await bot.edit_message_text(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                        f"{LEXICON_SHOP['1_attempt']}\n"
                                        f"{LEXICON_SHOP['20_attempt']}\n"
                                        f"{LEXICON_SHOP['100_attempt']}\n"  
                                        f"<b>БАЛАНС: {dust} пыли🌸</b>",
                                chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                reply_markup=create_inline_kb(1, 'shop_', 'Купить за пыль', 'Купить за деньги'))
    await callback.answer()
@router.message(StateFilter(FSMorder.name))
async def login_command(message: Message, state: FSMContext):
    if postreSQL_users(message.from_user.id):
        if postreSQL_login(message.text):
            await message.answer(text=f"{LEXICON_RU['login_user_true']}{message.text}", reply_markup=universe_kb)
            await state.clear()
        else:
            await message.answer(text=LEXICON_RU['login_user_false'])
    else:
        if postreSQL_login(message.text):
            await message.answer(text=LEXICON_RU['login_true'])
        else:
            await message.answer(text=f"{LEXICON_RU['login_false']}{message.text}", reply_markup=universe_kb)
            postreSQL_user_add(message.from_user.id, message.text)
            await state.clear()

@router.message(Text(text=LEXICON_RU['universe']))
async def add_universe(message: Message):
    inuverse = postgreSQL_all_universe()
    all_inuverse = list()
    for i in range(len(inuverse)):
        all_inuverse.append(inuverse[i][0])
    await message.answer(text='<u>ВЫБЕРИТЕ ВСЕЛЕНУЮ🪐</u>', reply_markup=create_inline_kb_universe_user(1, 'user_universe_', all_inuverse))



@router.callback_query(Text(startswith='user_universe_'))
async def menu_admin(callback: CallbackQuery):
    await callback.message.answer(text=f'Вы выбрали вселенную {callback.data.split("_")[-1]}', reply_markup= menu_user)
    postreSQL_universe_up(callback.data.split("_")[-1], callback.from_user.id)
    await callback.answer()


#Получить карту
@router.message(Text(text=LEXICON_RU['add_card']))
async def add_add_card_user(message: Message):
    user = postreSQL_users(message.from_user.id)
    ran = random.randint(1, 1001)
    difference = datetime.now() - datetime.strptime(user[-2], '%Y-%m-%d %H:%M:%S.%f')
    seconds = difference.total_seconds()
    minutes = seconds / 60
    hours = seconds / (60 * 60)
    attampts = int(user[5])
    if int(hours) >= 3:
        postreSQL_attempts_user_up(message.from_user.id, 1)
        postreSQL_data_user_up(message.from_user.id)
    if attampts <= 0:
        await message.answer(
            text=f'Вы уже получили карту\nСледующая попытка через: {(2-int(hours))} ч. {(59-(int(minutes) % 60))} мин.')
    else:
        if ran <= int(user[10]):
            await add_card_user(LEXICON_CARD_RARE['legendary'], message, user[3])
        elif ran <= int(user[9]):
            await add_card_user(LEXICON_CARD_RARE['mythical'], message, user[3])
        elif ran <= int(user[8]):
            await add_card_user(LEXICON_CARD_RARE['epic'], message, user[3])
        elif ran <= 150:
            await add_card_user(LEXICON_CARD_RARE['rare'], message, user[3])
        else:
            await add_card_user(LEXICON_CARD_RARE['usual'], message, user[3])

#Функция добавления карты
async def add_card_user(name_card, message, universe):
    cards = postreSQL_cards(name_card, universe)
    ran_card = random.randint(0, len(cards)-1)
    card_add = postgreSQL_add_card_user(message.from_user.id, cards[ran_card][1], cards[ran_card][3], universe)
    if card_add:
        card_print = postgreSQL_cards_one(card_add[3])
        if card_print[2].split('__')[0] == 'gif':
            await bot.send_animation(chat_id=message.from_user.id, animation=card_print[2].split('__')[1],
                                     caption=f'{card_print[1]}\n{LEXICON_CARD["attack"]} {cards[0][4]}\n '
                                             f'{LEXICON_CARD["health"]} {card_print[5]}\n '
                                             f'{LEXICON_CARD["value"]} {card_print[-2]}')
        else:
            await bot.send_photo(chat_id=message.from_user.id, photo=card_print[2].split('__')[1],
                                 caption=f'{card_print[1]}\n{LEXICON_CARD["attack"]} {cards[0][4]}\n '
                                         f'{LEXICON_CARD["health"]} {card_print[5]}\n ' f'{LEXICON_CARD["value"]} {card_print[-2]}')
    else:
        if name_card == LEXICON_CARD_RARE['legendary']:
            postgereSQL_dust_up(message.from_user.id, 150, LEXICON_CARD_RARE['legendary'])
            await message.answer(text='Карта которая выпала, у вас уже есть\n'
                                      'Вам начислено: 150 пыли🌸')
        elif name_card == LEXICON_CARD_RARE['mythical']:
            postgereSQL_dust_up(message.from_user.id, 70, LEXICON_CARD_RARE['mythical'])
            await message.answer(text='Карта которая выпала, у вас уже есть\n'
                                      'Вам начислено: 70 пыли🌸')
        elif name_card == LEXICON_CARD_RARE['epic']:
            postgereSQL_dust_up(message.from_user.id, 30, LEXICON_CARD_RARE['epic'])
            await message.answer(text='Карта которая выпала, у вас уже есть\n'
                                      'Вам начислено: 30 пыли🌸')
        elif name_card == LEXICON_CARD_RARE['rare']:
            postgereSQL_dust_up(message.from_user.id, 15, LEXICON_CARD_RARE['rare'])
            await message.answer(text='Карта которая выпала, у вас уже есть\n'
                                      'Вам начислено: 15 пыли🌸')
        else:
            postgereSQL_dust_up(message.from_user.id, 10, LEXICON_CARD_RARE['usual'])
            await message.answer(text='Карта которая выпала, у все уже есть\n'
                                      'Вам начислено: 10 пыли🌸')
    postreSQL_attempts_user_up(message.from_user.id, -1)
    postreSQL_data_user_up(message.from_user.id)



@router.message(Text(text='Мои карты'))
async def add_my_cards_user(message: Message):
    user = postreSQL_users(message.from_user.id)
    all_cards = postreSQL_cards_all_category(user[3])
    cards_user = postreSQL_cards_all_user_category(message.from_user.id, user[3])
    await message.answer(text='Ваши карты', reply_markup=create_inline_kb(1, 'cards_user_',
                                                                                            f"{LEXICON_CARD_RARE['usual']} {cards_user[0]}/{all_cards[0]}",
                                                                                            f"{LEXICON_CARD_RARE['rare']} {cards_user[1]}/{all_cards[1]}",
                                                                                            f"{LEXICON_CARD_RARE['epic']} {cards_user[2]}/{all_cards[2]}",
                                                                                            f"{LEXICON_CARD_RARE['mythical']} {cards_user[3]}/{all_cards[3]}",

                                                                                            f"{LEXICON_CARD_RARE['legendary']}  {cards_user[4]}/{all_cards[4]}"))
@router.callback_query(Text(startswith='cards_user_'))
async def cards_print_menu(callback: CallbackQuery):
    category = callback.data.split('_')[-1].split(' ')[0]
    user = postreSQL_users(callback.from_user.id)
    cards = postreSQL_cards(category, user[3])
    pg = int(postreSQL_pg_up(callback.from_user.id, -2))
    if cards[pg][1] in postreSQL_cards_all_user(callback.from_user.id):
        availability = 'ПОЛУЧЕНО❗️'
    else:
        availability = 'НЕ ПОЛУЧЕНО❗️'
    if len(cards) > 0:
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.send_animation(chat_id=callback.from_user.id, animation=cards[pg][2].split('__')[1],
                                                                    caption=f'{availability}\n{cards[pg][1]}\n{LEXICON_CARD["attack"]} {cards[pg][4]}\n '
                                                                            f'{LEXICON_CARD["health"]} {cards[pg][5]}\n '
                                                                       f'{LEXICON_CARD["value"]} {cards[pg][-2]}',
                                                                    reply_markup=create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.answer()
        else:
            await bot.send_photo(chat_id=callback.from_user.id,
                                            photo=cards[pg][2].split('__')[1],
                                            caption=f'{availability}\n{cards[pg][1]}\n{LEXICON_CARD["attack"]} {cards[pg][4]}\n {LEXICON_CARD["health"]} {cards[pg][5]}\n '
                                                                       f'{LEXICON_CARD["value"]} {cards[pg][-2]}',
                                            reply_markup=create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.answer()

    await callback.answer()


@router.callback_query(Text(startswith='user_forward_'))
async def process_forward_press(callback: CallbackQuery):
    user = postreSQL_users(callback.from_user.id)
    cards = postreSQL_cards(callback.data.split('_')[-1], user[3])
    pg = postreSQL_pg_up(callback.from_user.id, 0)
    len_pg = len(cards)
    if cards[pg][1] in postreSQL_cards_all_user(callback.from_user.id):
        availability = 'ПОЛУЧЕНО❗️'
    else:
        availability = 'НЕ ПОЛУЧЕНО❗️'
    if pg + 1 < len_pg:
        pg = postreSQL_pg_up(callback.from_user.id, 1)
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaAnimation(media=cards[pg][2].split('__')[1],
                                                               caption=f'{availability}\n{cards[pg][1]}\n{LEXICON_CARD["attack"]}: {cards[pg][4]}\n '
                                                                       f'{LEXICON_CARD["health"]} {cards[pg][5]}\n '
                                                                       f'{LEXICON_CARD["value"]} {cards[pg][-2]}'),
                                         reply_markup=create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
        else:
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=cards[pg][2].split('__')[1],
                                                               caption=f'{availability}\n{cards[pg][1]}\n{LEXICON_CARD["attack"]} {cards[pg][4]}\n '
                                                                       f'{LEXICON_CARD["health"]} {cards[pg][5]}\n '
                                                                       f'{LEXICON_CARD["value"]} {cards[pg][-2]}'),
                                         reply_markup=create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))

    await callback.answer()

@router.callback_query(Text(startswith='user_backward_'))
async def process_forward_press(callback: CallbackQuery):
    name_cards = callback.data.split('_')[-1]
    user = postreSQL_users(callback.from_user.id)
    cards = postreSQL_cards(name_cards,user[3])
    pg = int(postreSQL_pg_up(callback.from_user.id, 0))
    if cards[pg][1] in postreSQL_cards_all_user(callback.from_user.id):
        availability = 'ПОЛУЧЕНО❗️'
    else:
        availability = 'НЕ ПОЛУЧЕНО❗️'
    if pg > 0:
        pg = postreSQL_pg_up(callback.from_user.id, -1)
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaAnimation(media=cards[pg][2].split('__')[1],
                                         caption=f'{availability}\n{cards[pg][1]}\n{LEXICON_CARD["attack"]} {cards[pg][4]}\n '
                                                 f'{LEXICON_CARD["health"]} {cards[pg][5]}\n '
                                             f'{LEXICON_CARD["value"]} {cards[pg][-2]}'),
                                        reply_markup=create_pagination_keyboard(cards[pg][3],'backward',
                                                                                   f'{pg + 1}/{len(cards)}',
                                                                                   'forward'))
        else:
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=cards[pg][2].split('__')[1],
                                        caption=f'{availability}\n{cards[pg][1]}\n{LEXICON_CARD["attack"]} {cards[pg][4]}\n '
                                                f'{LEXICON_CARD["health"]} {cards[pg][5]}\n '
                                         f'{LEXICON_CARD["value"]} {cards[pg][-2]}'),
                                        reply_markup=create_pagination_keyboard(cards[pg][3], 'backward',
                                                                               f'{pg + 1}/{len(cards)}',
                                                                               'forward'))
    await callback.answer()

#ВОзвращение к выбору категории карточек
@router.callback_query(Text(text='назад_user'))
async def back_category_command(callback: CallbackQuery):
    user = postreSQL_users(callback.from_user.id)
    all_cards = postreSQL_cards_all_category(user[3])
    cards_user = postreSQL_cards_all_user_category(callback.from_user.id, user[3])
    await callback.message.answer(text='Ваши карты', reply_markup=create_inline_kb(1, 'cards_user_',
                                                                                            f"{LEXICON_CARD_RARE['usual']} {cards_user[0]}/{all_cards[0]}",
                                                                                            f"{LEXICON_CARD_RARE['rare']} {cards_user[1]}/{all_cards[1]}",
                                                                                            f"{LEXICON_CARD_RARE['epic']} {cards_user[2]}/{all_cards[2]}",
                                                                                            f"{LEXICON_CARD_RARE['mythical']} {cards_user[3]}/{all_cards[3]}",

                                                                                            f"{LEXICON_CARD_RARE['legendary']}  {cards_user[4]}/{all_cards[4]}"))
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()



#Ловим текст профиль
@router.message(Command(commands=['profile']))
async def add_my_cards_user(message: Message):
    user = postreSQL_users(message.from_user.id)
    all_cards = sum(postreSQL_cards_all_category(user[3]))
    cards_user = sum(postreSQL_cards_all_user_category(message.from_user.id, user[3]))

    user = postreSQL_users(message.from_user.id)
    all_points = sorted(postreSQL_point_all_user(), reverse=True)
    top = all_points.index(int(user[-1])) + 1
    await message.answer(text=f"🪐Вселенная: {user[3]}\n"
                              f"🃏Всего карт: {cards_user}/{all_cards}\n"
                              f"🔖Очки: {user[-1]}\n"
                              f"🎖Топ вселенной: {top} место\n"
                              f"🐢Логин: {user[2]}", reply_markup=create_inline_kb(1, 'change_', 'Сменить вселенную'))

@router.callback_query(Text(startswith='change_'))
async def process_forward_press(callback: CallbackQuery):
    inuverse = postgreSQL_all_universe()
    all_inuverse = list()
    for i in range(len(inuverse)):
        all_inuverse.append(inuverse[i][0])
    await callback.message.answer(text='<u>ВЫБЕРИТЕ ВСЕЛЕНУЮ🪐</u>',
                         reply_markup=create_inline_kb_universe_user(1, 'user_universe_', all_inuverse))
    await callback.answer()


@router.message(Command(commands=['shop']))
async def add_my_cards_user(message: Message):
    user = postreSQL_users(message.from_user.id)
    dust = user[4]
    await message.answer(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                f"{LEXICON_SHOP['1_attempt']}\n"
                                f"{LEXICON_SHOP['20_attempt']}\n"
                                f"{LEXICON_SHOP['100_attempt']}\n"                              
                                f"<b>БАЛАНС: {dust} пыли🌸</b>",
                         reply_markup=create_inline_kb(1, 'shop_', 'Купить за пыль', 'Купить за деньги'))




@router.callback_query(Text(text='shop_Купить за деньги'))
async def process_forward_press(callback: CallbackQuery):
    await bot.edit_message_text(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                "10 попытка - 50 рублей💵\n"
                                "30 попытка - 120 рублей💵\n"
                                "100 попытка - 450 рублей💵\n"
                                "За покупкой писать в лс: <a href='@Dekkuxx'>@Dekkuxx</a>",
                                chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                reply_markup=create_inline_kb(1, 'shop_', 'Магазин'))
    await callback.answer()
@router.callback_query(Text(text='shop_Магазин'))
async def add_my_cards_user(callback: CallbackQuery):
    user = postreSQL_users(callback.from_user.id)
    dust = user[4]
    await bot.edit_message_text(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                f"{LEXICON_SHOP['1_attempt']}\n"
                                f"{LEXICON_SHOP['20_attempt']}\n"
                                f"{LEXICON_SHOP['100_attempt']}\n"                              
                                f"<b>БАЛАНС: {dust} пыли🌸</b>",
                                chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                reply_markup=create_inline_kb(1, 'shop_', 'Купить за пыль', 'Купить за деньги'))
    await callback.answer()

@router.callback_query(Text(text='shop_Купить за пыль'))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text='Выбирите количество пыли🌸\n', chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                reply_markup=create_inline_kb(3, 'dust_shop_', '1', '20', '100', 'Отмена'))
    await state.set_state(FSMshop_dust.count)
    await callback.answer()

@router.callback_query(StateFilter(FSMshop_dust.count))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    user = postreSQL_users(callback.from_user.id)
    dust = int(user[4])
    coutn_dust = int(callback.data.split('_')[-1])
    if coutn_dust == 1:
        if dust > 74:
            await callback.message.answer('Вы приобрели 1 попытку')
            postgereSQL_dust_shop(callback.from_user.id, -75)
            postreSQL_attempts_user_up(callback.from_user.id, 1)
            user = postreSQL_users(callback.from_user.id)
            dust = int(user[4])
            await bot.edit_message_text(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                                f"{LEXICON_SHOP['1_attempt']}\n"
                                                f"{LEXICON_SHOP['20_attempt']}\n"
                                                f"{LEXICON_SHOP['100_attempt']}\n"  
                                                f"<b>БАЛАНС: {dust} пыли🌸</b>",
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, 'shop_', 'Купить за пыль', 'Купить за деньги'))
            await state.clear()
        else:
            await bot.edit_message_text(text='У вас не хватает пыли\n'
                                            'Выбирите количество пыли\n',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(3, 'dust_shop_', '1', '20', '100', 'Отмена'))
    elif coutn_dust == 20:
        if dust > 1499:
            await callback.message.answer('Вы приобрели 20 попыток')
            postgereSQL_dust_shop(callback.from_user.id, -1500)
            postreSQL_attempts_user_up(callback.from_user.id, 20)
            user = postreSQL_users(callback.from_user.id)
            dust = int(user[4])
            await bot.edit_message_text(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                             f"{LEXICON_SHOP['1_attempt']}\n"
                                            f"{LEXICON_SHOP['20_attempt']}\n"
                                            f"{LEXICON_SHOP['100_attempt']}\n"  
                                             f"<b>БАЛАНС: {dust} пыли🌸</b>",
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, 'shop_', 'Купить за пыль', 'Купить за деньги'))
            await state.clear()
            await callback.answer()
        else:
            await bot.edit_message_text(text='У вас не хватает пыли\n'
                                             'Выбирите количество пыли\n',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(3, 'dust_shop_', '1', '20', '100', 'Отмена'))
            await callback.answer()

    else:
        if dust > 7499:
            await callback.message.answer('Вы приобрели 100 попыток')
            user = postreSQL_users(callback.from_user.id)
            dust = int(user[4])
            postgereSQL_dust_shop(callback.from_user.id, -7500)
            postreSQL_attempts_user_up(callback.from_user.id, 100)
            await bot.edit_message_text(text=f"<u>{LEXICON_SHOP['shop']}</u>\n"
                                             f"{LEXICON_SHOP['1_attempt']}\n"
                                            f"{LEXICON_SHOP['20_attempt']}\n"
                                            f"{LEXICON_SHOP['100_attempt']}\n"  
                                             f"<b>БАЛАНС: {dust} пыли🌸</b>",
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, 'shop_', 'Купить за пыль', 'Купить за деньги'))
            await state.clear()
            await callback.answer()

        else:
            await bot.edit_message_text(text='У вас не хватает пыли\n'
                                             'Выбирите количество пыли\n',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(3, 'dust_shop_', '1', '20', '100', 'Отмена'))
    await callback.answer()


