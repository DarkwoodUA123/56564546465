import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv('API_ID').strip())
API_HASH = os.getenv('API_HASH').strip()
BOT_TOKEN = os.getenv('BOT_TOKEN').strip()
CHAT_ID = int(os.getenv('CHAT_ID').strip())

user_client = TelegramClient('user_session', API_ID, API_HASH)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

spam_task = None

async def spam_loop(text, count):
    try:
        for i in range(count):
            await user_client.send_message(CHAT_ID, text)
            print(f"[Спам] Сообщение #{i+1} отправлено: {text}")
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("Спам отменён пользователем.")
        raise

@bot_client.on(events.NewMessage(pattern=r'^/spam (\d+) (.+)'))
async def start_spam(event):
    global spam_task
    if spam_task and not spam_task.done():
        await event.reply("Спам уже запущен. Остановите текущий спам командой /stopspam.")
        return

    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)

    if count <= 0:
        await event.reply("Количество сообщений должно быть больше 0.")
        return
    if not text.strip():
        await event.reply("Текст спама не должен быть пустым.")
        return

    spam_task = asyncio.create_task(spam_loop(text, count))
    await event.reply(f"Запущен спам: {count} сообщений с текстом:\n{text}")

@bot_client.on(events.NewMessage(pattern='/stopspam'))
async def stop_spam(event):
    global spam_task
    if spam_task:
        spam_task.cancel()
        try:
            await spam_task
        except asyncio.CancelledError:
            pass
        spam_task = None
        await event.reply("Спам остановлен.")
    else:
        await event.reply("Спам не запущен.")

async def main():
    print("Запускаем user клиента...")
    await user_client.start()
    print("Запускаем bot клиента...")
    await bot_client.start(bot_token=BOT_TOKEN)
    print("Боты запущены. Ожидание команд...")

    await asyncio.gather(
        bot_client.run_until_disconnected(),
        user_client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())
