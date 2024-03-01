from Bot import bot, ACTIVE_QUIZZES
from Bot.db.users import add_user, id_to_username
from Bot.db.chats import add_chat
from Bot.utils.checks import is_admin
from Bot.utils.questions import get_question

import html
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton as Button
from pyrogram.types import InlineKeyboardMarkup as Markup

@bot.on_message(filters.command("quiz"))
async def quiz(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("You must be an admin to start a quiz.")
    if message.chat.id in ACTIVE_QUIZZES:
        return await message.reply_text("A quiz is already running in this chat.")
    ACTIVE_QUIZZES[message.chat.id] = {"users": [], "questions": [], "current_question": {}, "started": False}
    add_chat(message.chat.id)
    await message.reply_text("Quiz started! Send /endquiz to end the quiz.")
    xx = await bot.send_message(message.chat.id, "Starting quiz in 5 seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 4 seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 3 seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 2 seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 1 second...")
    await asyncio.sleep(1)
    await xx.delete()
    msg = None
    for i in range(3):
        question = await get_question()  # Get the next question
        text = question["question"]
        answers = question["options"]
        correct = question["correct"]
        ACTIVE_QUIZZES[message.chat.id]["questions"].append(question)
        ACTIVE_QUIZZES[message.chat.id]["current_question"] = question
        buttons = [[Button(html.unescape(answers[i]), f"answer_{i}")] for i in range(len(answers))]
        msg = await bot.send_message(message.chat.id, html.unescape(text), reply_markup=Markup(buttons))
        await asyncio.sleep(10)
        for user in ACTIVE_QUIZZES[message.chat.id]["users"]:
            user["answered"] = False
        if msg:
            await msg.delete()
    await bot.send_message(message.chat.id, "Quiz ended!")
    users = sorted(ACTIVE_QUIZZES[message.chat.id]["users"], key=lambda x: x["points"], reverse=True)[:10]
    text = "**Quiz results**:\n\n"
    for user in users:
        text += f"@{id_to_username(user['id'])}: `{user['points']} points`\n"
    await bot.send_message(message.chat.id, text)
    del ACTIVE_QUIZZES[message.chat.id]


@bot.on_callback_query(filters.regex(r"^answer_"))
async def answer(_, query):
    user = query.from_user.id
    chat = query.message.chat.id
    if chat not in ACTIVE_QUIZZES:
        return await query.answer("No active quiz in this chat.")
    userlist = [x["id"] for x in ACTIVE_QUIZZES[chat]["users"]]
    if user in userlist and [x for x in ACTIVE_QUIZZES[chat]["users"] if x["id"] == user][0]["answered"]:
        return await query.answer("You already answered this question.")
    if user not in userlist:
        user_data = {"id": user, "points": 0, "answered": True}
        ACTIVE_QUIZZES[chat]["users"].append(user_data)
        add_user(user, query.from_user.username)
    user_answer = ACTIVE_QUIZZES[chat]["current_question"]["options"][int(query.data.split("_")[1])]
    correct_answer = ACTIVE_QUIZZES[chat]["current_question"]["correct"]
    if user_answer == correct_answer:
        user = [x for x in ACTIVE_QUIZZES[chat]["users"] if x["id"] == user][0]
        user["points"] += 1
        user["answered"] = True
        ACTIVE_QUIZZES[chat]["users"][ACTIVE_QUIZZES[chat]["users"].index(user)] = user
        return await query.answer("Got your answer!")
    else:
        user = [x for x in ACTIVE_QUIZZES[chat]["users"] if x["id"] == user][0]
        user["answered"] = True
        ACTIVE_QUIZZES[chat]["users"][ACTIVE_QUIZZES[chat]["users"].index(user)] = user
        return await query.answer("Got your answer!")
    

       
     