from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from lexicon.lexicon_ru import LEXICON_RU
from data_base.postreSQL_bd import postreSQL_users, postreSQL_login, postreSQL_user_add
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
            await message.answer(text=f"{LEXICON_RU['login_user_true']}{message.text}")
            await state.clear()
        else:
            await message.answer(text=LEXICON_RU['login_user_false'])
    else:
        if postreSQL_login(message.text):
            await message.answer(text=LEXICON_RU['login_true'])
        else:
            await message.answer(text=f"{LEXICON_RU['login_false']}{message.text}")
            postreSQL_user_add(message.from_user.id, message.text)
            await state.clear()


    # if message.from_user.id in users:
    #     await state.update_data(name=message.text)

