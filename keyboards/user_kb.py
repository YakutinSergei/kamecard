from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_ADMIN, LEXICON_SHOP


def create_inline_kb(width: int,
                     pref: str,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=pref + button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=pref + button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

def create_inline_kb_universe_user(width: int,
                     pref: str,
                     name_inuverse: list) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs

    for button in name_inuverse:
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=f'{pref}_{button}'))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()



def create_pagination_keyboard(name_card: str, user_id: int,  *buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_ADMIN[button] if button in LEXICON_ADMIN else button,
        callback_data=f'user_{button}_{user_id}_{name_card}') for button in buttons]).row(InlineKeyboardButton(text='НАЗАД', callback_data=f'назад_user_{user_id}'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


btn_universe: KeyboardButton = KeyboardButton(text=LEXICON_RU['universe'])
btn_add_card: KeyboardButton = KeyboardButton(text=LEXICON_RU['add_card'])
btn_my_cards: KeyboardButton = KeyboardButton(text=LEXICON_RU['my_cards'])
menu_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(width=2, keyboard=[[btn_add_card], [btn_my_cards]],
                                                    resize_keyboard=True)
universe_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_universe]],
                                                    resize_keyboard=True)

