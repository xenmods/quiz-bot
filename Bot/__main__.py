from Bot import bot, LOGGER
from Bot.modules import *
from Bot.db import *
from Bot.config import Config
from pyrogram import idle
import asyncio

loop = asyncio.get_event_loop()

async def main():
    LOGGER.info("Starting Bot...")
    await bot.start()
    LOGGER.info("Bot Started.")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER.info("--------------------Bot Stopped--------------------")