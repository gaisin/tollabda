import asyncio
import os
from telegram import Bot

TG_SECRET = os.environ.get('TG_SECRET')
TG_CHANNEL_ID = os.environ.get('TG_CHANNEL_ID')


async def send_message_to_channel(message):
    bot = Bot(token=TG_SECRET)
    await bot.send_message(chat_id=TG_CHANNEL_ID, text=message)
