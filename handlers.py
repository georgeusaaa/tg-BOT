from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import random

router = Router()
user_scores = {}
user_questions = {}

# Клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Викторина')],
        [KeyboardButton(text='Случайный факт')],
        [KeyboardButton(text='Добавить факт')]
    ],
    resize_keyboard=True
)

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

# Факты
default_facts = [
    'В фильме "Один дома" Кевин МакКаллистер мог сам звонить в полицию, но сценаристы решили, что это "неинтересно".',
    'В "Титанике" ледокол, который должен был столкнуться с кораблем, на самом деле был не ледоколом, а исследовательским судном.',
    'В "Властелине колец" орки на самом деле были очень дружелюбными актерами, которые часто играли в карты между съемками.',
    'В "Джокере" персонаж Хоакина Феникса вдохновлен "Таксистом" Мартина Скорсезе, где Роберт Де Ниро сыграл роль похожую на Джокера.',
    'Фильм "Кавказская пленница, или Новые приключения Шурика" снимался в Крыму, а многие сцены, которые должны были быть в горах, были сняты в павильонах.'
]

questions = [
    ('В каком году сняли фильм «Один дома»?', 'Один дома'),
    ('Кто на самом деле рисовал Розу в «Титанике»?', 'Титаник'),
    ('Где снимали трилогию «Властелин колец»?', 'Властелин колец'),
    ('Какой актер не играл «Джокера»?', 'Джокер'),
    ('Как называется фильм на фото?', 'Фото')
]

questions_and_answers = {
    '1990_г_один_дома': 'Правильно, +1 балл',
    '1980_г_один_дома': 'Неправильно, +0 баллов',
    'кети_бейтс_титаник': 'Неправильно, +0 баллов',
    'джемс_кемерон_титаник': 'Правильно, +1 балл',
    'в_ирландии_властелин_колец': 'Неправильно, +0 баллов',
    'в_новой_зеландии_властелин_колец': 'Правильно, +1 балл',
    'шон_пенн_джокер': 'Правильно, +1 балл',
    'марк_хэмилл_джокер': 'Неправильно, +0 баллов',
    'кавказская_пленница_фото': 'Правильно, +1 балл',
    'операция_ы_фото': 'Неправильно, +0 баллов'
}


# State
class AddFact(StatesGroup):
    add_fact = State()


@router.message(Command('start'))
async def start_bot(message: Message):
    user_id = message.from_user.id
    if user_id not in user_scores:
        user_scores[user_id] = 0
    if user_id not in user_questions:
        user_questions[user_id] = 0
    await message.answer(
        text='Здравствуйте, я бот по фильмам! Могу дать вам викторину или интересные факты про разные фильмы!',
        reply_markup=main
    )


async def ask_question(message: Message, user_id: int):
    question_num = user_questions.get(user_id, 0)
    if question_num < len(questions):
        question_text, film_key = questions[question_num]
        if film_key == 'Фото':
            await message.answer_photo(
                photo='AgACAgIAAxkBAAIBpWZ2iSjsZDVeAh-79KnB2brXsG1kAAJS2TEbZMa4S2pUm5SrISYhAQADAgADeQADNQQ'
            )
        await message.answer(text=question_text, reply_markup=question_buttons[film_key])
    else:
        score = user_scores.get(user_id, 0)
        await message.answer(f'Викторина окончена! Ваш балл: {score}')
        user_questions[user_id] = 0
        user_scores[user_id] = 0


@router.message(F.text == 'Викторина')
async def send_question(message: Message):
    user_id = message.from_user.id
    user_questions[user_id] = 0
    user_scores[user_id] = 0
    await ask_question(message, user_id)


@router.callback_query()
async def send_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    answer = questions_and_answers.get(callback.data)

    if answer:
        await callback.message.answer(answer)
        if 'Правильно' in answer:
            user_scores[user_id] = user_scores.get(user_id, 0) + 1

        if user_id in user_questions:
            user_questions[user_id] += 1
        else:
            user_questions[user_id] = 1

        await ask_question(callback.message, user_id)
        await callback.answer()
    else:
        await callback.message.answer(text='Некорректный ответ')
        await callback.answer()


@router.message(F.text == 'Случайный факт')
async def send_fact(message: Message):
    random_fact = random.choice(default_facts)
    await message.answer(text=random_fact)


@router.message(F.text == 'Добавить факт')
async def add_fact(message: Message, state: FSMContext):
    await message.answer(text="Напишите свой факт о фильмах!")
    await state.set_state(AddFact.add_fact)


@router.message(AddFact.add_fact, F.text)
async def fact_added(message: Message, state: FSMContext):
    default_facts.append(message.text)
    await message.answer(text="Ваш факт успешно добавлен!")
    await state.clear()


@router.message()
async def handle_unknown(message: Message):
    await message.answer(text="Используйте кнопки для навигации!")