from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from create_bot import bot
from data_base.promo_db import promo_add, all_promo, promo_user
from keyboards.admin_kb import create_inline_kb

from lexicon.lexicon_ru import LEXICON_CARD, LEXICON_PROMO, LEXICON_CARD_RARE, LEXICON_RU

router: Router = Router()


class FSMAdmin_promo(StatesGroup):
    promocode = State()
    validity = State()
    number_attempts = State()

class FSMUser_promo(StatesGroup):
    promocode = State()


@router.callback_query(Text(text=LEXICON_CARD['promo']))
async def promo(callback: CallbackQuery):
    print('nen')
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, 'promo_',
                                                                      LEXICON_PROMO['add'],
                                                                      LEXICON_PROMO['listPromo'],
                                                                      LEXICON_RU['back']))
    await callback.answer()

@router.callback_query(Text(startswith='promo_'))
async def promo_list(callback: CallbackQuery, state: FSMContext):
    if callback.data.split('_')[-1] == LEXICON_PROMO['add']:
        await callback.message.answer(text="Ввеведи промокод")
        await state.set_state(FSMAdmin_promo.promocode)
        await callback.answer()

    elif callback.data.split('_')[-1] == LEXICON_PROMO['listPromo']:
        all_promos = await all_promo()
        print_promo = ''
        for i in range(len(all_promos)):
            print_promo +=(f'Промокод: {all_promos[i]["promocode"]}\n'
                               f'Использования: {all_promos[i]["validity"]}\n'
                               f'Попытки: {all_promos[i]["number_attempts"]}\n'
                               f'_____________________________\n\n')
        await callback.message.answer(text=print_promo)
        await callback.answer()
    else:
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


@router.message(StateFilter(FSMAdmin_promo.promocode))
async def process_name_card(message: Message, state: FSMContext):
    await state.update_data(promocode=message.text)
    await message.answer(text="Введи количество использований")
    await state.set_state(FSMAdmin_promo.validity)


@router.message(StateFilter(FSMAdmin_promo.validity))
async def process_name_card(message: Message, state: FSMContext):
    await state.update_data(validity=message.text)
    await message.answer(text="Введи количество попыток, которое дается при вводе промокода")
    await state.set_state(FSMAdmin_promo.number_attempts)

@router.message(StateFilter(FSMAdmin_promo.number_attempts))
async def process_name_card(message: Message, state: FSMContext):
    await state.update_data(number_attempts=message.text)
    promo = await state.get_data()
    await state.clear()
    print(promo)
    await promo_add(promo)
    await message.answer(text="✅Промокод успешно добавлен")


# Если в чате ввел промокод
@router.message(Text(text=['Ввести промокод', 'ввести промокод', 'ВВЕСТИ ПРОМОКОД']))
async def promo_input(message: Message, state: FSMContext):
    await state.set_state(FSMUser_promo.promocode)
    await bot.send_message(chat_id=message.chat.id, text='Введите промокод')


@router.message(StateFilter(FSMUser_promo.promocode))
async def input_user_promo(message: Message, state: FSMContext):
    promo = await promo_user(message.text, message.from_user.id)
    if promo[0]:
        if promo[1]:
            await bot.send_message(chat_id=message.chat.id, text="✅Промокод успешно активирован\n"
                                      f"Добавлено попыток: {promo[0]['number_attempts']}")
        else:
            await bot.send_message(chat_id=message.chat.id, text="❌Вы уже активировали этот промокод")
    else:
        await bot.send_message(chat_id=message.chat.id, text="❌Такого промокода нет")



    await state.clear()
