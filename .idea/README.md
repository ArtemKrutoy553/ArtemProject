# 🤖 Telegram ChatGPT Bot

Telegram-бот на Python с использованием библиотеки `aiogram`, который позволяет общаться с ChatGPT (модель GPT-4o) и распознавать голосовые сообщения через Whisper API от OpenAI.

---

## 🚀 Функционал

- Общение с ChatGPT по тексту
- Распознавание голосовых сообщений (Whisper) и их отправка в GPT
- Асинхронная обработка запросов
- Простая настройка и запуск

---

## 🧰 Технологии

- Python 3.10+
- aiogram 3.20.0.post0
- OpenAI API (GPT-4o и Whisper)
- aiohttp для загрузки голосовых сообщений
- dotenv для работы с переменными окружения

---

## Установка и запуск

  

```bash
git clone https://github.com/ArtemKrutoy553/ArtemProject.git
cd ArtemProject
pip install -r requirements.txt
TELEGRAM_TOKEN=ваш_токен_бота_от_BotFather
OPENAI_API_KEY=ваш_ключ_OpenAI_API
python bot.py
plaintext:
Пользователь: Расскажи анекдот про программистов
Бот: Почему программисты не любят природу? Там слишком много багов!
