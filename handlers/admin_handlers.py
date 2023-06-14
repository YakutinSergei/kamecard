from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto,  InputMediaAnimation
from aiogram import Router, F
from aiogram.filters import Command, Text
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_CARD, LEXICON_CARD_RARE
from aiogram.fsm.storage.memory import MemoryStorage
from create_bot import bot
from data_base.postreSQL_bd import postreSQL_admin, postreSQL_card_add, postreSQL_cards, postreSQL_login, postreSQL_pg_up, \
    postreSQL_del_cards, postreSQL_dust_up
from data_base.postgreSQL_bd_universal import postreSQL_universe_add, postgreSQL_all_universe
from keyboards.admin_kb import create_inline_kb, admin_create_pagination_keyboard, create_inline_kb_universe


router: Router = Router()

class FSMAdmin_card(StatesGroup):
    name = State()
    attack = State()
    protection = State()
    rare = State()
    img = State()

class FSMAdmin_universal(StatesGroup):
    name = State()

class FSMAdmin_dust(StatesGroup):
    login = State()
    attempts = State()

@router.message(Text(text='Отмена'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Вы и не начинали добавлять')
    await bot.edit_message_text(text='МЕНЮ АДМИНИСТРАТОРА', chat_id=message.from_user.id,
                                message_id=message.message_id,
                                reply_markup=create_inline_kb(1, '',
                                                              LEXICON_CARD['card'],
                                                              LEXICON_CARD['add_card'],
                                                              LEXICON_CARD['universe'],
                                                              LEXICON_CARD['add_inuverse'],
                                                              LEXICON_CARD['add_attempt']))


@router.message(Text(text='Отмена'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Добавление отменено')
    await bot.edit_message_text(text='МЕНЮ АДМИНИСТРАТОРА', chat_id=message.from_user.id,
                                message_id=message.message_id,
                                reply_markup=create_inline_kb(1, '',
                                                              LEXICON_CARD['card'],
                                                              LEXICON_CARD['add_card'],
                                                              LEXICON_CARD['universe'],
                                                              LEXICON_CARD['add_inuverse'],
                                                              LEXICON_CARD['add_attempt']))
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()



@router.message(Command(commands=['admin']))
async def process_moderator_command(message: Message):
    if postreSQL_admin(message.from_user.id):
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot.send_message(message.from_user.id, text='МЕНЮ АДМИНИСТРАТОРА', reply_markup=create_inline_kb(1,'',
                                                                                                               LEXICON_CARD['card'],
                                                                                                               LEXICON_CARD['add_card'],
                                                                                                               LEXICON_CARD['universe'],
                                                                                                               LEXICON_CARD['add_inuverse'],
                                                                                                               LEXICON_CARD['add_attempt']))
    else:
        await bot.send_message(message.from_user.id, text='Вы не являетесь администратором')
#region Дабавление карточки
@router.callback_query(Text(text=LEXICON_CARD['add_card']))
async def process_add_card_command(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer(text="Введи имя карточки:")
    await state.set_state(FSMAdmin_card.name)
    await callback.answer()

# Функция добавления имени карточки
@router.message(StateFilter(FSMAdmin_card.name))
async def process_name_card(message: Message, state: FSMContext):
    await state.update_data(neme=message.text)
    await message.answer(text="Введи значение атаки карточки:")
    await state.set_state(FSMAdmin_card.attack)

# Функция добавления атаки карточки
@router.message(StateFilter(FSMAdmin_card.attack))
async def process_attack_card(message: Message, state: FSMContext):
    await state.update_data(attack=message.text)
    await message.answer(text="Введи значение защиты карточки:")
    await state.set_state(FSMAdmin_card.protection)

# Функция добавления защиты карточки
@router.message(StateFilter(FSMAdmin_card.protection))
async def process_protection_card(message: Message, state: FSMContext):
    await state.update_data(protection=message.text)
    await state.update_data(protection=message.text)
    await message.answer(text="Выберите редкость", reply_markup=create_inline_kb(1, '',
                                                                                 LEXICON_CARD_RARE['usual'],
                                                                                 LEXICON_CARD_RARE['rare'],
                                                                                 LEXICON_CARD_RARE['epic'],
                                                                                 LEXICON_CARD_RARE['mythical'],
                                                                                 LEXICON_CARD_RARE['legendary']))
    await state.set_state(FSMAdmin_card.rare)


# Функция добавления редкости
@router.callback_query(StateFilter(FSMAdmin_card.rare))
async def process_rare_card(calllback: CallbackQuery, state: FSMContext):
    await state.update_data(rare=calllback.data)
    await calllback.message.answer(text="Загрузите фото карточки")
    await state.set_state(FSMAdmin_card.img)

# Функция добавления фото
@router.message(StateFilter(FSMAdmin_card.img))
async def process_rare_card(message: Message, state: FSMContext):
    if message.animation:
        file_info = await bot.get_file(message.document.file_id)
        await state.update_data(img='gif__'+file_info.file_id)
        new_card = await state.get_data()
        await state.clear()
        print(new_card)
        postreSQL_card_add(new_card)
        await message.answer(text='Карта успешно добавлена', reply_markup=create_inline_kb(1,'',
                                                                                           LEXICON_CARD['card'],
                                                                                           LEXICON_CARD['add_card'],
                                                                                           LEXICON_CARD['universe'],
                                                                                           LEXICON_CARD['add_inuverse'],
                                                                                           LEXICON_CARD['add_attempt']))
    elif message.photo:
        await state.update_data(img='photo__' + message.photo[0].file_id)
        new_card = await state.get_data()
        await state.clear()
        postreSQL_card_add(new_card)
        print(new_card)
        await message.answer(text='Карта успешно добавлена', reply_markup=create_inline_kb(1, '',
                                                                                           LEXICON_CARD['card'],
                                                                                           LEXICON_CARD['add_card'],
                                                                                           LEXICON_CARD['universe'],
                                                                                           LEXICON_CARD['add_inuverse'],
                                                                                           LEXICON_CARD['add_attempt']))
    else:
        await message.answer(text='Отправили что то не то')

#endregion

#region Показ карточек
@router.callback_query(Text(text=LEXICON_CARD['card']))
async def process_add_card_command(callback: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, 'cards_',
                                                                      LEXICON_CARD_RARE['usual'],
                                                                      LEXICON_CARD_RARE['rare'],
                                                                      LEXICON_CARD_RARE['epic'],
                                                                      LEXICON_CARD_RARE['mythical'],
                                                                      LEXICON_CARD_RARE['legendary'],
                                                                      LEXICON_RU['back']))
    await callback.answer()



@router.callback_query(Text(text=['cards_НАЗАД', 'universe_НАЗАД']))
async def cards_print_menu(callback: CallbackQuery):
    await bot.edit_message_text(text='МЕНЮ АДМИНИСТРАТОРА', chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=create_inline_kb(1, '',
                                                              LEXICON_CARD['card'],
                                                              LEXICON_CARD['add_card'],
                                                              LEXICON_CARD['universe'],
                                                              LEXICON_CARD['add_inuverse'],
                                                              LEXICON_CARD['add_attempt']))
    await callback.answer()

@router.callback_query(Text(startswith='cards_'))
async def cards_print_menu(callback: CallbackQuery):
    cards = postreSQL_cards(callback.data.split('_')[-1])
    print(cards)
    pg = int(postreSQL_pg_up(callback.from_user.id, -2))
    if len(cards) > 0:
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.send_animation(chat_id=callback.from_user.id, animation=cards[pg][2].split('__')[1],
                                                                    caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                                                       f'Ценность: {cards[pg][-1]}',
                                                                    reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.answer()
        else:
            print('тут')
            await bot.send_photo(chat_id=callback.from_user.id,
                                            photo=cards[pg][2].split('__')[1],
                                            caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                                                       f'Ценность: {cards[pg][-1]}',
                                            reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
            await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
            await callback.answer()

    await callback.answer()

@router.callback_query(Text(startswith='admin_forward_'))
async def process_forward_press(callback: CallbackQuery):
    cards = postreSQL_cards(callback.data.split('_')[-1])
    pg = postreSQL_pg_up(callback.from_user.id, 0)
    print(pg)
    len_pg = len(cards)
    print(len_pg)
    if pg + 1 < len_pg:
        pg = postreSQL_pg_up(callback.from_user.id, 1)
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaAnimation(media=cards[pg][2].split('__')[1],
                                                               caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                                                       f'Ценность: {cards[pg][-1]}'),
                                         reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
        else:
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=cards[pg][2].split('__')[1],
                                                               caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                                                       f'Ценность: {cards[pg][-1]}'),
                                         reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
        #await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


    await callback.answer()

@router.callback_query(Text(startswith='admin_backward_'))
async def process_forward_press(callback: CallbackQuery):
    name_cards = callback.data.split('_')[-1]
    print(name_cards)
    cards = postreSQL_cards(name_cards)
    pg = int(postreSQL_pg_up(callback.from_user.id, 0))
    len_pg = len(cards)
    if pg > 0:
        pg = postreSQL_pg_up(callback.from_user.id, -1)
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaAnimation(media=cards[pg][2].split('__')[1],
                                         caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                             f'Ценность: {cards[pg][-1]}'),
                                        reply_markup=admin_create_pagination_keyboard(cards[pg][3],'backward',
                                                                                   f'{pg + 1}/{len(cards)}',
                                                                                   'forward'))
        else:
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=cards[pg][2].split('__')[1],
                                        caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                         f'Ценность: {cards[pg][-1]}'),
                                        reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                               f'{pg + 1}/{len(cards)}',
                                                                               'forward'))
    await callback.answer()

#ВОзвращение к выбору категории карточек
@router.callback_query(Text(text='назад_admin'))
async def back_category_command(callback: CallbackQuery):
    await callback.message.answer(text='МЕНЮ АДМИНИСТРАТОРА', reply_markup=create_inline_kb(1, 'cards_',
                                                                      LEXICON_CARD_RARE['usual'],
                                                                      LEXICON_CARD_RARE['rare'],
                                                                      LEXICON_CARD_RARE['epic'],
                                                                      LEXICON_CARD_RARE['mythical'],
                                                                      LEXICON_CARD_RARE['legendary'],
                                                                      LEXICON_RU['back']))
    await callback.answer()

@router.callback_query(Text(startswith='удалить_admin_'))
async def del_product_command(callback: CallbackQuery):
    name_cards = callback.data.split('_')[-1]
    cards = postreSQL_cards(name_cards)
    pg = int(postreSQL_pg_up(callback.from_user.id, 0))
    postreSQL_del_cards(cards[pg][1])
    cards.pop(pg)
    len_pg = len(cards)
    if len_pg == 0:
        await bot.send_message(callback.from_user.id, text='МЕНЮ АДМИНИСТРАТОРА', reply_markup=create_inline_kb(1, '',
                                                                                                                LEXICON_CARD['card'],
                                                                                                                LEXICON_CARD['add_card'],
                                                                                                                LEXICON_CARD['universe'],
                                                                                                                LEXICON_CARD['add_inuverse'],
                                                                                                                LEXICON_CARD['add_attempt']))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.answer()
    else:

        pg = postreSQL_pg_up(callback.from_user.id, -1)
        if cards[pg][2].split('__')[0] == 'gif':
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaAnimation(media=cards[pg][2].split('__')[1],
                                                                   caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                                                           f'Ценность: {cards[pg][-1]}'),
                                         reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))
        else:
            await bot.edit_message_media(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                         media=InputMediaPhoto(media=cards[pg][2].split('__')[1],
                                                               caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                                                       f'Ценность: {cards[pg][-1]}'),
                                         reply_markup=admin_create_pagination_keyboard(cards[pg][3], 'backward',
                                                                                       f'{pg + 1}/{len(cards)}',
                                                                                       'forward'))

    await callback.answer()
#endregion


#region Дабавление вселенных

#Написание имени
@router.callback_query(Text(text=LEXICON_CARD['add_inuverse']))
async def process_add_card_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите название вселенной')
    await state.set_state(FSMAdmin_universal.name)
    await callback.answer()

#Запись в базу
@router.message(StateFilter(FSMAdmin_universal.name))
async def process_name_card(message: Message, state: FSMContext):
    await state.update_data(neme=message.text)
    postreSQL_universe_add(message.text)
    await message.answer(text="Вселенная успешно добавлена", reply_markup=create_inline_kb(1,'',
                                                                                           LEXICON_CARD['card'],
                                                                                           LEXICON_CARD['add_card'],
                                                                                           LEXICON_CARD['universe'],
                                                                                           LEXICON_CARD['add_inuverse'],
                                                                                           LEXICON_CARD['add_attempt']))
    await state.clear()

@router.callback_query(Text(text=LEXICON_CARD['universe']))
async def process_add_universe_command(callback: CallbackQuery):
    inuverse = postgreSQL_all_universe()
    all_inuverse = list()
    for i in range(len(inuverse)):
        all_inuverse.append(inuverse[i][0])
    all_inuverse.append('НАЗАД')
    await bot.edit_message_text(text='ВСЕЛЕННЫЕ', chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                reply_markup=create_inline_kb_universe(1, 'universe', all_inuverse))
    await callback.answer()


#Ввод логина для добавления пыли
@router.callback_query(Text(text=LEXICON_CARD['add_attempt']))
async def process_add_login_dust_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите логин пользователя')
    await state.set_state(FSMAdmin_dust.login)


# Ввод количества пыли
@router.message(StateFilter(FSMAdmin_dust.login))
async def process_add_dust_command(message: Message, state: FSMContext):
    login = postreSQL_login(message.text)
    if login:
        await state.update_data(login=message.text)
        await message.answer('Введите количество попыток')
        await state.set_state(FSMAdmin_dust.attempts)
    else:
        await message.answer('Вы указали не существующий логин')


#Добавление в БД
@router.message(StateFilter(FSMAdmin_dust.attempts), lambda x: x.text.isdigit())
async def process_add_dust_sql(message: Message, state: FSMContext):
    await state.update_data(attempts=message.text)
    add_dust=await state.get_data()
    await state.clear()
    print(add_dust)
    postreSQL_dust_up(add_dust)
    await message.answer(text='Попытки успешно добавлены')
    await bot.send_message(message.from_user.id, text='МЕНЮ АДМИНИСТРАТОРА', reply_markup=create_inline_kb(1, '',
                                                                                                           LEXICON_CARD['card'],
                                                                                                           LEXICON_CARD['add_card'],
                                                                                                           LEXICON_CARD['universe'],
                                                                                                           LEXICON_CARD['add_inuverse'],
                                                                                                           LEXICON_CARD['add_attempt']))

#Некоректный ввод
@router.message(StateFilter(FSMAdmin_dust.attempts))
async def process_add_dust_sql(message: Message, state: FSMContext):
    await message.answer('Вы указали не верное значение попыток')

#endregion
