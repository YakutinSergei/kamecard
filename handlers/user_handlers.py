from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from data_base.postgreSQL_bd_universal import postgreSQL_all_universe
from lexicon.lexicon_ru import LEXICON_RU
from data_base.postreSQL_bd import postreSQL_users, postreSQL_login, postreSQL_user_add
from keyboards.user_kb import create_inline_kb, universe_kb, create_inline_kb_universe_user
from create_bot import bot


router: Router = Router()

class FSMorder(StatesGroup):
    name = State()

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/start'])
    await state.set_state(FSMorder.name)


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
    await message.answer(text='<u>ВЫБЕРИТЕ ВСЕЛЕНУЮ</u>', reply_markup=create_inline_kb_universe_user(1, 'user_universe', all_inuverse))


