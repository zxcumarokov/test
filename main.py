
import hashlib # берет сторку и возвращает закодированую строку используе для id
from aiogram import Bot, Dispatcher, executor, types, Bot  # mid
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  # keyboards
from aiogram.utils.callback_data import CallbackData  # cb filter
import random
import asyncio
import re
from collections import defaultdict

TOKEN = '5991863328:AAHf0Fyz3rtMR8851RF3xfyqdzIYNNDbVnM'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def assign_random_numbers(accounts):
    result = []
    for acc in accounts:
        random_numbers = [random.randint(1, 100) for _ in range(5)]
        result.append(f"{acc} {' '.join(map(str, random_numbers))}")
    return result

tg_acc = ["@zxcebajlak231", "@master_74", "@mood_breaker", "@zahar4ik_scam"]
random_assigned = assign_random_numbers(tg_acc)

def get_keybord() -> InlineKeyboardMarkup: #создаем клавы в сообщении которые при нажатии создают каллбекдату
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                'отправить',
                callback_data = 'ok',
                url="https://t.me/+g_Om0C25L7g3ODFi"
            )],
        ]
    )
    return ikb

# @dp.message_handler()
# async def all_msg_handler(message: types.Message):
#     reply_text = "Ответ на сообщение..."
#     await message.reply(reply_text, reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(commands=['add'])
async def cmd_add_account(message: types.Message):
    new_account = message.text.split()[1]  # Получаем новый аккаунт из текста сообщения

    if new_account.startswith('@'):  # Проверяем, что аккаунт начинается с символа @
        tg_acc.append(new_account)  # Добавляем новый аккаунт в массив tg_acc
        random_assigned.append(assign_random_numbers([new_account])[0])  # Генерируем для нового аккаунта случайные числа
        await message.answer(f"Аккаунт {new_account} был успешно добавлен.")
    else:
        await message.answer("Ошибка: аккаунт должен начинаться с символа @.")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    user_id = message.from_user.id
    user = message.from_user

    for _ in range(1):
        for item in random_assigned:
            if user.username and user.username in item:
                formatted_item = f'👑 {item}'  # Добавляем emoji короны к аккаунту пользователя
            else:
                formatted_item = item
            await message.answer(formatted_item, reply_markup=get_keybord())
        await message.answer("🐸🐸🐸*Это все аккаунты*🐸🐸🐸  ", parse_mode='MarkdownV2')
        await asyncio.sleep(30)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def process_random_numbers(message: types.Message):
    user_id = message.from_user.id
    user = message.from_user
    # Создаем словарь для хранения сгенерированных чисел и связанных с ними аккаунтов
    generated_numbers = defaultdict(list)

    # Заполняем словарь сгенерированными числами и аккаунтами
    for item in random_assigned:
        parts = item.split()  # Разделяем строку на части
        account = parts[0]  # Получаем аккаунт
        numbers = list(map(int, parts[1:]))  # Получаем числа и преобразуем их в список целых чисел
        generated_numbers[account] = numbers

    # Проверяем, что сообщение начинается с нужного префикса
    if message.text.startswith("♻️ Генератор случайных чисел:"):
        numbers = re.findall(r'\d+', message.text)
        numbers_list = [int(num) for num in numbers]
        matched_numbers = set()  # Множество для хранения уже совпавших чисел

        # Сравниваем числа сгенерированные пользователем с числами в словаре
        for account, generated in generated_numbers.items():
            matches = sum(1 for num in numbers_list if num in generated and num not in matched_numbers)

            # Проверяем, является ли текущий аккаунт аккаунтом пользователя
            account_username = account[1:] if account.startswith('@') else account
            crown = '' if account_username == user.username else ''  # Добавляем знак короны, если это аккаунт пользователя

            if matches >= 0:
                matched_numbers.update([num for num in numbers_list if num in generated])
                await message.answer(
                    f"{crown}{account} {' '.join(map(str, generated))} совпадения {matches}/5 совпало число {', '.join(map(str, [num for num in numbers_list if num in generated and num not in matched_numbers]))}")
                if matches >= 5:
                    await message.answer(f"{crown}{account} {' '.join(map(str, generated))} бинго")


@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'ok':
        return await callback.answer(text='красавчик')
    return await callback.answer('2 текст всплывающего сообщения')

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True
    )



