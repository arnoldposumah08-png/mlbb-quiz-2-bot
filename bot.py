from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
from question import QUESTIONS
from rank import get_rank
import database
import random

user_data = {}

# ================= UTIL ==================

def group_only(update):
    return update.effective_chat.type in ["group", "supergroup"]

# ================= START ==================

def start(update, context):
    if update.effective_chat.type == "private":

        keyboard = [
            [InlineKeyboardButton("Dev", url="https://t.me/yasanyamagurai")],
            [InlineKeyboardButton("Tambahkan ke GRUP", url="https://t.me/quizmlbb2_bot?startgroup=true")]
        ]

        update.message.reply_text(
            "Halo Player, Selamat datang di QUIZ MLBB 2 🎯\n"
            "Game tebak kata tanpa gambar!\n\n"
            "Gunakan /start di grup untuk mulai.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if not group_only(update):
        return

    chat_id = str(update.effective_chat.id)

    if chat_id in user_data and user_data[chat_id].get("active"):
        update.message.reply_text("⚠️ Game masih berjalan!")
        return

    # 🔥 SHUFFLE SEKALI DI AWAL
    shuffled = random.sample(QUESTIONS, len(QUESTIONS))

    user_data[chat_id] = {
        "active": True,
        "questions": shuffled,
        "index": 0,
        "current_q": None,
        "answered": False,
        "answered_by": {},
        "hint_used": [],
        "last_q_msg": None
    }

    send_question(update, context)

# ================= RENDER ==================

def build_question_text(user):
    q = user["current_q"]
    answers = q["answers"]

    text = "🎯 QUIZ MLBB\n\n"

    for i, a in enumerate(answers):
        if i in user["answered_by"]:
            text += f"{i+1}. {a} (+10) [{user['answered_by'][i]}]\n"
        else:
            text += f"{i+1}. ______\n"

    text += "\nSilahkan /next Jika soalnya susah bosque^^"
    text += "\natau bisa gunakan /nyerah untuk spill Jawaban^^"

    return text

# ================= GAME ==================

def send_question(update, context):
    chat_id = str(update.effective_chat.id)
    user = user_data[chat_id]

    # 🔥 JIKA HABIS → RESET + SHUFFLE ULANG
    if user["index"] >= len(user["questions"]):
        user["questions"] = random.sample(QUESTIONS, len(QUESTIONS))
        user["index"] = 0

    q = user["questions"][user["index"]]
    user["index"] += 1

    user["current_q"] = q
    user["answered"] = False
    user["answered_by"] = {}
    user["hint_used"] = []

    text = build_question_text(user)

    msg = context.bot.send_message(chat_id=int(chat_id), text=text)
    user["last_q_msg"] = msg.message_id

# ================= REFRESH ==================

def refresh_question(context, chat_id):
    user = user_data[chat_id]

    text = build_question_text(user)

    msg = context.bot.send_message(chat_id=int(chat_id), text=text)

    try:
        if user.get("last_q_msg"):
            context.bot.delete_message(chat_id=int(chat_id), message_id=user["last_q_msg"])
    except:
        pass

    user["last_q_msg"] = msg.message_id

# ================= JAWAB ==================

def answer(update, context):
    if not group_only(update):
        return

    if not update.message or not update.message.text:
        return

    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)

    first = update.effective_user.first_name or ""
    last = update.effective_user.last_name or ""
    name = f"{first} {last}".strip()

    user_answer = update.message.text.lower().strip()

    if chat_id not in user_data:
        return

    user = user_data[chat_id]

    if not user.get("active") or user.get("answered"):
        return

    q = user.get("current_q")
    answers = q["answers"]

    for idx, ans in enumerate(answers):
        if user_answer == ans.lower():

            if idx in user["answered_by"]:
                return

            user["answered_by"][idx] = name

            try:
                database.add_global_score(user_id, name, 10)
                database.add_group_score(chat_id, user_id, name, 10)
            except Exception as e:
                print("DB ERROR:", e)

            refresh_question(context, chat_id)
            break

    # 🔥 AUTO LANJUT SOAL BARU
    if len(user["answered_by"]) == len(answers):
        user["answered"] = True

        context.bot.send_message(
            chat_id=int(chat_id),
            text="🎉 Semua jawaban terjawab! Soal berikutnya..."
        )

        send_question(update, context)

# ================= NEXT ==================

def next_q(update, context):
    if not group_only(update):
        return

    chat_id = str(update.effective_chat.id)

    if chat_id not in user_data or not user_data[chat_id].get("active"):
        update.message.reply_text("⚠️ Game belum dimulai!")
        return

    send_question(update, context)

# ================= NYERAH ==================

def nyerah(update, context):
    if not group_only(update):
        return

    chat_id = str(update.effective_chat.id)
    user_id = str(update.effective_user.id)

    if chat_id not in user_data:
        return

    user = user_data[chat_id]

    if user_id in user["hint_used"]:
        update.message.reply_text("❌ Kamu sudah pakai bocoran di soal ini!")
        return

    q = user.get("current_q")
    answers = q["answers"]

    for idx, ans in enumerate(answers):
        if idx not in user["answered_by"]:
            user["answered_by"][idx] = "🤖 bot"
            user["hint_used"].append(user_id)
            break

    refresh_question(context, chat_id)

# ================= LEADERBOARD ==================

def leaderboard(update, context):
    if not group_only(update):
        return

    data = database.get_global_leaderboard()

    if not data:
        update.message.reply_text("Belum ada data leaderboard.")
        return

    text = "🏆 LEADERBOARD GLOBAL 🏆\n\n"

    for i, (name, score) in enumerate(data, start=1):
        rank_name = get_rank(score)
        text += f"{i}. {name} — {rank_name} ({score})\n"

    update.message.reply_text(text)

# ================= RUN ==================

def main():
    database.init_db()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", next_q))
    dp.add_handler(CommandHandler("nyerah", nyerah))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    print("BOT MLBB 2 RUNNING...")

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
