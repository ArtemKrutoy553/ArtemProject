import os
import asyncio
import tempfile
import aiohttp


from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# === ТВОИ КЛЮЧИ ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Настройка клиентов ===
bot = Bot(
    token=TELEGRAM_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
client = OpenAI(api_key=OPENAI_API_KEY)

# === Функция общения с GPT ===
async def ask_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === Обработка голосовых сообщений ===
@dp.message(F.voice)
async def handle_voice(message: Message):
    print("🔊 Обработчик голосового сообщения вызван")

    voice = message.voice
    file = await bot.get_file(voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file.file_path}"

    try:
        # Скачивание аудиофайла
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as response:
                    temp_audio.write(await response.read())
                    temp_path = temp_audio.name

        # Транскрибация через Whisper
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        os.remove(temp_path)

        if transcript and transcript.text:
            gpt_response = await ask_openai(transcript.text)
            await message.answer(gpt_response)
        else:
            await message.answer("Не удалось распознать голосовое сообщение 😕")

    except Exception as e:
        print(f"Ошибка при обработке голосового: {e}")
        await message.answer("Произошла ошибка при обработке голосового сообщения 😢")


@dp.message(F.text)
async def handle_text(message: Message):
    prompt = message.text
    response = await ask_openai(prompt)
    await message.answer(response)

# === Запуск бота ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
