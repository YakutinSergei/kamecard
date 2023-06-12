from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import Router, F
from aiogram.filters import Command, Text
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_CARD, LEXICON_CARD_RARE
from aiogram.fsm.storage.memory import MemoryStorage
from create_bot import bot
from data_base.postreSQL_bd import postreSQL_admin, postreSQL_card_add, postreSQL_cards
from keyboards.admin_kb import create_inline_kb, admin_create_pagination_keyboard


router: Router = Router()

class FSMAdmin_card(StatesGroup):
    name = State()
    attack = State()
    protection = State()
    rare = State()
    img = State()

@router.message(Text(text='Отмена'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Вы и не начинали добавлять')


@router.message(Text(text='Отмена'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Добавление отменено')
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
        await state.update_data(img='gif_'+file_info.file_id)
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
        await state.update_data(img='photo_' + message.photo[0].file_id)
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

@router.callback_query(Text(startswith='cards_'))
async def cards_print_menu(callback: CallbackQuery):
    cards = postreSQL_cards(callback.data.split('_')[-1])
    print(cards)
    pg = 0
    if len(cards) > 0:
        if cards[pg][2].split('_')[0] == 'gif':
            await bot.send_animation(chat_id=callback.from_user.id, animation=cards[pg][2].split('_')[1],
                                 caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                         f'Ценность: {cards[pg][-1]}',
                                 reply_markup= admin_create_pagination_keyboard('backward',
                                                                               f'{pg + 1}/{len(cards)}',
                                                                               'forward'))
        else:
            await bot.send_photo(chat_id=callback.from_user.id, photo=cards[pg][2].split('_')[1],
                                 caption=f'{cards[pg][1]}\nАтака: {cards[pg][4]}\n Защита: {cards[pg][5]}\n '
                                         f'Ценность: {cards[pg][-1]}',
                                 reply_markup= admin_create_pagination_keyboard('backward',
                                                                               f'{pg + 1}/{len(cards)}',
                                                                               'forward'))

@router.callback_query(Text(text='admin_forward'))
async def process_forward_press(callback: CallbackQuery):
    cards = postreSQL_cards(callback.data.split('_')[-1])
    res = postreSQL_read(user_up[0][2])
    len_pg = len(res)
    if int(user_up[0][3]) + 1 < len_pg:
        pg = postreSQL_pg_up(callback.from_user.id, 1)
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(media=res[pg][2],
                                  caption=f'{res[pg][3]}\nОписание: {res[pg][4]}\n Цена:{res[pg][-1]}'),
            reply_markup=admin_create_pagination_keyboard('backward',
                                                    f'{pg + 1}/{len_pg}',
                                                    'forward'))

    await callback.answer()

@router.callback_query(Text(text='admin_backward'))
async def process_forward_press(callback: CallbackQuery):
    user_up = postreSQL_user_read(callback.from_user.id)
    res = postreSQL_read(user_up[0][2])
    len_pg = len(res)
    if int(user_up[0][3]) > 0:
        pg = postreSQL_pg_up(callback.from_user.id, -1)
        if pg < len_pg:
            await bot.edit_message_media(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                media=InputMediaPhoto(media=res[pg][2],
                                      caption=f'{res[pg][3]}\nОписание: {res[pg][4]}\n Цена:{res[pg][-1]}'),
                reply_markup=admin_create_pagination_keyboard('backward',
                                                              f'{pg + 1}/{len_pg}',
                                                              'forward'))

    await callback.answer()
#endregion

