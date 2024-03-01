from Bot import bot
from Bot.db.chats import get_all_chats
from Bot.db.users import get_all_users

from time import time
from pyrogram import filters

@bot.on_message(filters.command("ping"))
async def ping(_, message):
    start = time()
    msg = await message.reply_text("Pong!")
    end = time()
    await msg.edit_text(f"Pong! `{round((end - start) * 1000, 2) }ms`")

@bot.on_message(filters.command("qstats"))
async def qstats(_, message):
    chats = get_all_chats()
    users = get_all_users()
    await message.reply_text(f"**Chats:** {len(chats)}\n**Users:** {len(users)}")