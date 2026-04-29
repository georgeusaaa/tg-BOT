from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Викторина')],
        [KeyboardButton(text='Случайный факт')],
        [KeyboardButton(text='Добавить факт')]
    ],
    resize_keyboard=True
)

# Клавиатуры для вопросов викторины
question_buttons = {
    'Один дома': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='1990', callback_data='1990_г_один_дома')],
        [InlineKeyboardButton(text='1980', callback_data='1980_г_один_дома')]
    ]),
    'Титаник': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Кэти Бейтс', callback_data='кети_бейтс_титаник')],
        [InlineKeyboardButton(text='Джеймс Кэмерон', callback_data='джемс_кемерон_титаник')]
    ]),
    'Властелин колец': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='В Ирландии', callback_data='в_ирландии_властелин_колец')],
        [InlineKeyboardButton(text='В Новой Зеландии', callback_data='в_новой_зеландии_властелин_колец')]
    ]),
    'Джокер': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Шон Пенн', callback_data='шон_пенн_джокер')],
        [InlineKeyboardButton(text='Марк Хэмилл', callback_data='марк_хэмилл_джокер')]
    ]),
    'Фото': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Кавказская пленница', callback_data='кавказская_пленница_фото')],
        [InlineKeyboardButton(text='Операция Ы', callback_data='операция_ы_фото')]
    ])
}