from Bot import bot
from Bot.db.users import add_user

from pyrogram import filters
from pyrogram.types import Message

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("Hello! I'm a quiz bot.")
    add_user(message.from_user.id, message.from_user.username)

@bot.on_message(filters.command("help"))
async def help(_, message: Message):
    await message.reply_text("I'm a quiz bot.\nAdd me to a group and make me admin to start a quiz.")
    add_user(message.from_user.id, message.from_user.username)

