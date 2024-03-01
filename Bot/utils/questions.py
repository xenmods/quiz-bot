from Bot import session

async def get_question():
    resp = await session.get("https://opentdb.com/api.php?amount=1&category=31&type=multiple")
    data = resp.json()
    return {
        "question": data["results"][0]["question"],
        "options": data["results"][0]["incorrect_answers"] + [data["results"][0]["correct_answer"]],
        "correct": data["results"][0]["correct_answer"]}
