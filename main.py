import asyncio
import datetime
import os

import asyncpg
from dotenv import load_dotenv
from loguru import logger
from telethon import TelegramClient

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
client = TelegramClient("anon", api_id, api_hash)

CHANNELS = ["exploitex"]

logger.add(
    "parser.log",
    format="{time} {level} {message}",
    level="INFO",
    rotation="50 MB",
    compression="zip",
)


class Parser:
    async def start(self, channel):
        conn = await self.get_connection()

        async for message in client.iter_messages(channel, limit=50):
            if not await self.is_message_exists(
                message.id, str(message.peer_id.channel_id), conn
            ):
                await self.save_message(message, conn)

        await conn.close()

    async def get_connection(self):
        return await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
        )

    async def save_message(self, message, conn):
        date = datetime.datetime.strptime(str(message.date)[:-6], "%Y-%m-%d %H:%M:%S")
        await conn.execute(
            """
                INSERT INTO telegram_posts(channel_id, message_id, published_at, text, views)
                VALUES($1, $2, $3, $4, $5)
            """,
            str(message.peer_id.channel_id),
            message.id,
            date,
            message.text,
            message.views,
        )

    async def is_message_exists(self, message_id: int, channel_id: str, conn) -> bool:
        result = await conn.fetch(
            """
                SELECT * FROM telegram_posts WHERE message_id = $1 AND channel_id = $2
            """,
            message_id,
            channel_id,
        )

        return bool(result)


async def main():
    while True:
        for channel in CHANNELS:
            try:
                await Parser().start(channel)
                logger.info(f"Сообщения из {channel} успешно обработаны")
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщений из {channel}: {e}")
        await asyncio.sleep(3600)


with client:
    client.loop.run_until_complete(main())
