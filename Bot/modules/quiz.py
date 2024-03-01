from Bot import bot, ACTIVE_QUIZZES
from Bot.db.users import add_user, id_to_username, add_score, get_top_users
from Bot.db.chats import add_chat
from Bot.utils.checks import is_admin
from Bot.utils.questions import get_question
from Bot.utils.formatting import format_time

import html
import asyncio
from time import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton as Button
from pyrogram.types import InlineKeyboardMarkup as Markup

@bot.on_message(filters.command("startquiz"))
async def quiz(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("You must be an admin to start a quiz.")
    if message.chat.id in ACTIVE_QUIZZES:
        return await message.reply_text("A quiz is already running in this chat.")
    args = message.text.split(" ", 1)
    if len(args) > 1:
        if args[1].isdigit():
            if int(args[1]) < 1 or int(args[1]) > 10:
                return await message.reply_text("Invalid number of questions. Must be between **1 and 10**.")
            else:
                number = int(args[1])
        else:
            return await message.reply_text("Invalid number of questions. Must be a number between **1 and 10**.")
    else:
        return await message.reply_text("You must specify the number of questions.")
    ACTIVE_QUIZZES[message.chat.id] = {"users": [], "questions": [], "current_question": {}, "started": False, "last_question_time": 0}
    add_chat(message.chat.id)
    await message.reply_text("Quiz started! Send /endquiz to end the quiz.")
    xx = await bot.send_message(message.chat.id, "Starting quiz in 5️⃣ seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 4️⃣ seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 3️⃣ seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 2️⃣ seconds...")
    await asyncio.sleep(1)
    await xx.edit_text("Starting quiz in 1️⃣ second...")
    await asyncio.sleep(1)
    await xx.delete()
    await bot.send_message(message.chat.id, "**LET'S GO! 🚀**")
    await bot.send_message(message.chat.id, "Quiz started! You have **10 seconds** to answer each question.")
    for i in range(number):
        prev_questions = [q['question'] for q in ACTIVE_QUIZZES[message.chat.id]["questions"]]
        question = await get_question()  # Get the next question
        tries = 0
        while question["question"] in prev_questions and tries < 5:
            question = await get_question()
            tries += 1
        text = question["question"]
        answers = question["options"]
        correct = question["correct"]
        ACTIVE_QUIZZES[message.chat.id]["questions"].append(question)
        ACTIVE_QUIZZES[message.chat.id]["current_question"] = question
        buttons = [[Button(html.unescape(answers[i]), f"answer_{i}")] for i in range(len(answers))]
        msg = await bot.send_message(message.chat.id, html.unescape(text), reply_markup=Markup(buttons))
        ACTIVE_QUIZZES[message.chat.id]["last_question_time"] = time()
        await asyncio.sleep(10)
        if message.chat.id not in ACTIVE_QUIZZES:
            return
        for user in ACTIVE_QUIZZES[message.chat.id]["users"]:
            user["answered"] = False
        buttons = []
        correct_answers = 0
        for answer in answers:
            if answer == correct:
                buttons.append([Button(f"✅ {html.unescape(answer)}", "none")])
                correct_answers = [x for x in ACTIVE_QUIZZES[message.chat.id]["users"] if answer in x["correct_answers"]]
            else:
                buttons.append([Button(html.unescape(answer), "none")])
        text += f"\nThe correct answer was: **{correct}**\n`{len(correct_answers)}` users answered correctly!"
        await msg.edit(text=text, reply_markup=Markup(buttons))
    await bot.send_message(message.chat.id, "Quiz ended!")
    users = sorted(ACTIVE_QUIZZES[message.chat.id]["users"], key=lambda x: x["points"], reverse=True)[:10]
    text = "🏁 **The quiz has ended!**:\n\n"
    text += f"__**{number}** questions answered.__\n\n"
    get_prefix = lambda x: "🥇" if x == 0 else "🥈" if x == 1 else "🥉" if x == 2 else f"{x + 1}."
    y = 0
    for user in users:
        add_score(user["id"], user["points"])
        average_time = int(user["total_time"] / number)
        text += f"{get_prefix(y)} @{id_to_username(user['id'])}: **{user['points']}** ({format_time(average_time)})\n"
        y += 1

    text += "\n**🏆 Thanks for participating!**"
    await bot.send_message(message.chat.id, text, reply_markup=Markup([[Button("Quiz Bot", url="iacquizbot.t.me")]]))
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
        user_data = {"id": user, "points": 0, "answered": True, "correct_answers": [], "total_time": 0}
        ACTIVE_QUIZZES[chat]["users"].append(user_data)
        add_user(user, query.from_user.username)
    user_answer = ACTIVE_QUIZZES[chat]["current_question"]["options"][int(query.data.split("_")[1])]
    correct_answer = ACTIVE_QUIZZES[chat]["current_question"]["correct"]
    if user_answer == correct_answer:
        user = [x for x in ACTIVE_QUIZZES[chat]["users"] if x["id"] == user][0]
        user["total_time"] += time() - ACTIVE_QUIZZES[chat]["last_question_time"]
        user["points"] += 1
        user["answered"] = True
        user["correct_answers"].append(user_answer)
        ACTIVE_QUIZZES[chat]["users"][ACTIVE_QUIZZES[chat]["users"].index(user)] = user
        return await query.answer("Got your answer!")
    else:
        user = [x for x in ACTIVE_QUIZZES[chat]["users"] if x["id"] == user][0]
        user["total_time"] += time() - ACTIVE_QUIZZES[chat]["last_question_time"]
        user["answered"] = True
        ACTIVE_QUIZZES[chat]["users"][ACTIVE_QUIZZES[chat]["users"].index(user)] = user
        return await query.answer("Got your answer!")
    
@bot.on_message(filters.command("endquiz"))
async def end_quiz(_, message: Message):
    if not await is_admin(message):
        return await message.reply_text("You must be an admin to end a quiz.")
    if message.chat.id in ACTIVE_QUIZZES:
        del ACTIVE_QUIZZES[message.chat.id]
        return await message.reply_text("Quiz ended.")
    else:
        return await message.reply_text("No active quiz in this chat.")
     

@bot.on_message(filters.command("nerds"))
async def top(_, message: Message):
    users = get_top_users()
    text = "🏆 **Top 10 users**:\n\n"
    get_prefix = lambda x: "🥇" if x == 0 else "🥈" if x == 1 else "🥉" if x == 2 else f"{x + 1}."
    y = 0
    for user in users:
        text += f"{get_prefix(y)} @{user.username}: **{user.score}** points\n"
        y += 1
    await message.reply_text(text, reply_markup=Markup([[Button("Quiz Bot", url="t.me/iacquizbot")]]))