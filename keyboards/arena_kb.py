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
            callback_data=LEXICON_ARENA['search'])
        btn_teams: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['teams'],
            callback_data=LEXICON_ARENA['teams'])
        btn_statistics: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['statistics'],
            callback_data=LEXICON_ARENA['statistics'])
    else:
        btn_search: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['no_search'],
            callback_data=LEXICON_ARENA['no_search'])
        btn_teams: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['teams'],
            callback_data=LEXICON_ARENA['teams'])
        btn_statistics: InlineKeyboardButton = InlineKeyboardButton(
            text=LEXICON_ARENA['statistics'],
            callback_data=LEXICON_ARENA['statistics'])

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
            callback_data='btn_card_1')
    else:
        btn_card_1: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data='btn_card_1')


    if teams['card_2_name'] != 'Пусто':
        btn_card_2: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data='btn_card_2')
    else:
        btn_card_2: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data='btn_card_2')

    if teams['card_3_name'] != 'Пусто':
        btn_card_3: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data='btn_card_3')
    else:
        btn_card_3: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data='btn_card_3')


    if teams['card_4_name'] != 'Пусто':
        btn_card_4: InlineKeyboardButton = InlineKeyboardButton(
            text='✅',
            callback_data='btn_card_4')
    else:
        btn_card_4: InlineKeyboardButton = InlineKeyboardButton(
            text='❌',
            callback_data='btn_card_4')

    btn_back: InlineKeyboardButton = InlineKeyboardButton(
        text='🔙Назад',
        callback_data='back_arena')

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(btn_card_1, btn_card_2, btn_card_3, btn_card_4, width=4).row(btn_back, width=1)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
