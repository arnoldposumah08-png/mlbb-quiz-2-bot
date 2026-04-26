def answer(update, context):
    if not group_only(update):
        return

    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name or "User"

    if chat_id not in user_data:
        return

    user = user_data[chat_id]

    if not user.get("active") or user.get("answered"):
        return

    msg = update.message.text.lower()
    inputs = [x.strip() for x in msg.replace("\n", ",").split(",") if x.strip()]

    q = user["current_q"]
    answers = [a.lower() for a in q["answers"]]

    updated = False

    for inp in inputs:
        if inp in answers:

            idx = answers.index(inp)

            if idx in user["answered_by"]:
                continue

            user["answered_by"][idx] = name
            updated = True

            try:
                database.add_global_score(user_id, name, 25)
                database.add_group_score(chat_id, user_id, name, 25)
            except:
                pass

    if updated:
        refresh_question(context, chat_id)

    if len(user["answered_by"]) == len(answers):
        user["answered"] = True
        context.bot.send_message(chat_id=int(chat_id), text="➡️ Soal baru...")
        send_question(update, context)
