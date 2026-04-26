from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
from generator import generate_question
from rank import get_rank
import database

user_data = {}

# ================= UTIL ==================

def group_only(update):
    return update.effective_chat and update.effective_chat.type in ["group", "supergroup"]

def normalize(text):
    return text.lower().strip()


# ================= START ==================

def start(update, context):
    chat = update.effective_chat

    if chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("Dev", url="https://t.me/yasanyamagurai")],
            [InlineKeyboardButton("Tambahkan ke GRUP", url="https://t.me/quizmlbb2_bot?startgroup=true")]
        ]

        update.message.reply_text(
            "🎯 QUIZ MLBB 2\n\nTambahkan bot ini ke grup untuk mulai bermain!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    chat_id = str(chat.id)

    if chat_id in user_data and user_data[chat_id].get("active"):
        update.message.reply_text("⚠️ Game masih berjalan!")
        return

    user_data[chat_id] = {
        "active": True,
        "current_q": None,
        "answered": False,
        "answered_by": {},
        "hint_used": set(),
        "last_q_msg": None
    }

    send_question(update, context)


# ================= QUESTION ==================

def build_question_text(user):
    q = user["current_q"]

    text = f"❓ {q['question']}\n\n"
    text += "✍️ Ketik jawaban kamu (bisa lebih dari 1, pisahkan dengan koma)\n"

    if not user["answered"]:
        text += "\n💡 /next untuk skip\n💡 /nyerah untuk bantuan"
    else:
        text += "\n\n🎉 Semua terjawab!"

    return text


# ================= SEND QUESTION ==================

def send_question(update, context):
    chat_id = str(update.effective_chat.id)

    if chat_id not in user_data:
        return

    user = user_data[chat_id]

    q = generate_question()
    if not q:
        return send_question(update, context)

    user["current_q"] = q
    user["answered"] = False
    user["answered_by"] = {}
    user["hint_used"] = set()

    text = build_question_text(user)

    msg = context.bot.send_message(chat_id=int(chat_id), text=text)
    user["last_q_msg"] = msg.message_id


# ================= REFRESH ==================

def refresh_question(context, chat_id):
    try:
        user = user_data.get(chat_id)
        if not user:
            return

        text = build_question_text(user)

        msg = context.bot.send_message(chat_id=int(chat_id), text=text)

        old = user.get("last_q_msg")
        if old:
            try:
                context.bot.delete_message(chat_id=int(chat_id), message_id=old)
            except:
                pass

        user["last_q_msg"] = msg.message_id

    except Exception as e:
        print("REFRESH ERROR:", e)


# ================= ANSWER ==================

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

    msg = normalize(update.message.text)

    q = user["current_q"]
    answers = [normalize(a) for a in q["answers"]]

    inputs = [x.strip() for x in msg.replace("\n", ",").split(",") if x.strip()]

    updated = False

    for inp in inputs:
        inp = normalize(inp)

        for idx, ans in enumerate(answers):
            if inp == ans:

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


# ================= NEXT ==================

def next_q(update, context):
    chat_id = str(update.effective_chat.id)

    if chat_id not in user_data:
        update.message.reply_text("⚠️ Game belum dimulai!")
        return

    send_question(update, context)


# ================= NYERAH ==================

def nyerah(update, context):
    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)

    if chat_id not in user_data:
        return

    user = user_data[chat_id]

    if user_id in user["hint_used"]:
        update.message.reply_text("❌ Sudah pakai bantuan!")
        return

    q = user["current_q"]

    for idx, ans in enumerate(q["answers"]):
        if idx not in user["answered_by"]:
            user["answered_by"][idx] = "🤖 bot"
            user["hint_used"].add(user_id)
            break

    refresh_question(context, chat_id)


# ================= LEADERBOARD ==================

def leaderboard(update, context):
    data = database.get_global_leaderboard()

    if not data:
        update.message.reply_text("Belum ada data.")
        return

    text = "🏆 GLOBAL LEADERBOARD\n\n"

    for i, (name, score) in enumerate(data, 1):
        text += f"{i}. {name} — {get_rank(score)} ({score})\n"

    update.message.reply_text(text)


# ================= GROUP TOP ==================

def topgrup(update, context):
    chat_id = str(update.effective_chat.id)
    data = database.get_group_leaderboard(chat_id)

    if not data:
        update.message.reply_text("Belum ada data grup.")
        return

    text = "🏆 LEADERBOARD GRUP\n\n"

    for i, (name, score) in enumerate(data, 1):
        text += f"{i}. {name} — {get_rank(score)} ({score})\n"

    update.message.reply_text(text)


# ================= STATS ==================

def stats(update, context):
    user_id = str(update.effective_user.id)

    score = database.get_user_score(user_id) or 0

    update.message.reply_text(
        f"📊 STATS\n\n"
        f"🔥 MMR: {score}\n"
        f"🏆 RANK: {get_rank(score)}"
    )


# ================= MAIN ==================

def main():
    database.init_db()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", next_q))
    dp.add_handler(CommandHandler("nyerah", nyerah))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(CommandHandler("topgrup", topgrup))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    print("BOT MLBB RUNNING...")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
