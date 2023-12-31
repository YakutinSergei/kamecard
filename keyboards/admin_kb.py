from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_ADMIN


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



def admin_create_pagination_keyboard(name_card: str, *buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_ADMIN[button] if button in LEXICON_ADMIN else button,
        callback_data=f'admin_{button}_{name_card}') for button in buttons]).row(InlineKeyboardButton(text='УДАЛИТЬ', callback_data=f'удалить_admin_{name_card}')).row(InlineKeyboardButton(text='НАЗАД', callback_data='назад_admin'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_inline_kb_universe(width: int,
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