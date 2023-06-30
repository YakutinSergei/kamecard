from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_ADMIN, LEXICON_ARENA


def arena_menu_kb(teams) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    if teams['ful']:
        btn_search: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['search'],
            callback_data=LEXICON_ARENA['search']+f'_{teams["user_id"]}')
        btn_teams: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['teams'],
            callback_data=LEXICON_ARENA['teams']+f'_{teams["user_id"]}')
        btn_statistics: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['statistics'],
            callback_data=LEXICON_ARENA['statistics']+f'_{teams["user_id"]}')
    else:
        btn_search: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['no_search'],
            callback_data=LEXICON_ARENA['no_search']+f'_{teams["user_id"]}')
        btn_teams: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['teams'],
            callback_data=LEXICON_ARENA['teams']+f'_{teams["user_id"]}')
        btn_statistics: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['statistics'],
            callback_data=LEXICON_ARENA['statistics']+f'_{teams["user_id"]}')

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(btn_search, width=1).row(btn_teams, btn_statistics, width=2)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def arena_teams_kb(teams):
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []


    if teams['card_1_name'] != 'Пусто':
        btn_card_1: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data=f'btn_card_1__{teams["user_id"]}')
    else:
        btn_card_1: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data=f'btn_card_1__{teams["user_id"]}')


    if teams['card_2_name'] != 'Пусто':
        btn_card_2: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data=f'btn_card_2__{teams["user_id"]}')
    else:
        btn_card_2: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data=f'btn_card_2__{teams["user_id"]}')

    if teams['card_3_name'] != 'Пусто':
        btn_card_3: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data=f'btn_card_3__{teams["user_id"]}')
    else:
        btn_card_3: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data=f'btn_card_3__{teams["user_id"]}')


    if teams['card_4_name'] != 'Пусто':
        btn_card_4: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data=f'btn_card_4__{teams["user_id"]}')
    else:
        btn_card_4: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data=f'btn_card_4__{teams["user_id"]}')

    btn_back: InlineKeyboardButton = InlineKeyboardButton(
        text='🔙Назад',
        callback_data=f'back_arena__{teams["user_id"]}')

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(btn_card_1, btn_card_2, btn_card_3, btn_card_4, width=4).row(btn_back, width=1)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_pag_keyboard_arena(user_id: int, categore: str, *buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_ADMIN[button] if button in LEXICON_ADMIN else button,
        callback_data=f'ar_{button}_{user_id}_{categore}') for button in buttons]).row(InlineKeyboardButton(text='✅ВЫБРАТЬ',
                                                                                                               callback_data=f'choice_{user_id}_{categore}')).\
        row(InlineKeyboardButton(text='🔙НАЗАД', callback_data=f'back_Card_{user_id}_{categore}'))
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_inline_kb_arena(width: int,
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
                callback_data='card_arena_'+pref + button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=pref + button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()