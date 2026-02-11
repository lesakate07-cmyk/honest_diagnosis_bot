import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, GOOGLE_FORM_URL
from states import TestState
from questions import QUESTIONS, OPTIONS
from keyboards import answer_keyboard, start_keyboard, offer_keyboard
from results import get_result

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_answers = {}

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Привет. Это честная диагностика твоей точки А.",
        reply_markup=start_keyboard()
    )

@dp.message(F.text == "Начать диагностику")
async def q1(message: Message, state: FSMContext):
    user_answers[message.from_user.id] = []
    await state.set_state(TestState.q1)
    await message.answer(QUESTIONS[0], reply_markup=answer_keyboard(OPTIONS[0]))

@dp.message(TestState.q1)
async def q_handler(message: Message, state: FSMContext):
    user_answers[message.from_user.id].append(message.text[0])
    current = list(TestState).index(await state.get_state())
    
    if current < 6:
        await state.set_state(list(TestState)[current + 1])
        await message.answer(
            QUESTIONS[current + 1],
            reply_markup=answer_keyboard(OPTIONS[current + 1])
        )
    else:
        result = get_result(user_answers[message.from_user.id])
        await state.clear()
        await message.answer(result, reply_markup=offer_keyboard())

@dp.message(F.text == "Хочу на 3 дня")
async def offer(message: Message):
    await message.answer(
        f"Оставь предзапись здесь:\n{GOOGLE_FORM_URL}"
    )

@dp.message(F.text == "Пока подумаю")
async def wait(message: Message):
    await message.answer(
        "Ты можешь вернуться в любой момент 🤍"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
