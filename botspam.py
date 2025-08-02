import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))

user_client = TelegramClient('user_session', API_ID, API_HASH)
bot_client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Твой остальной код без изменений...

async def main():
    print("Запускаем user клиента...")
    await user_client.start()  # сессия уже есть, ввод не нужен
    print("Запускаем bot клиента...")
    await bot_client.start()
    print("Боты запущены. Ожидание команд...")

    await asyncio.gather(
        bot_client.run_until_disconnected(),
        user_client.run_until_disconnected()
    )

if __name__ == '__main__':
    asyncio.run(main())
