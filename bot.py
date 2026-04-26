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
    total = len(q["answers"])

    text = f"❓ {q['question']}\n\n"

    for i in range(total):
        if i in user["answered_by"]:
            hero = q["answers"][i]
            player = user["answered_by"][i]
            text += f"{i+1}. {hero} (+25) [{player}]\n"
        else:
            text += f"{i+1}. ______\n"

    if not user["answered"]:
        text += "\nSilahkan /next jika soalnya susah bosque^^"
        text += "\natau gunakan /nyerah untuk spill jawaban^^"
    else:
        text += "\n\n🎉 Semua jawaban terjawab! Soal berikutnya.."

    return text


# ================= SEND ==================

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

    # anti duplicate mapping
    answer_map = {normalize(a): i for i, a in enumerate(q["answers"])}

    inputs = [x.strip() for x in msg.replace("\n", ",").split(",") if x.strip()]

    updated = False

    for inp in inputs:
        inp = normalize(inp)

        if inp not in answer_map:
            continue

        idx = answer_map[inp]

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

    # ✅ AUTO NEXT FIX
    if len(user["answered_by"]) == len(q["answers"]):
        user["answered"] = True

        # tampilkan notif selesai dulu
        refresh_question(context, chat_id)

        # lanjut soal baru
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


# ================= MAIN ==================

def main():
    database.init_db()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("next", next_q))
    dp.add_handler(CommandHandler("nyerah", nyerah))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    print("BOT MLBB RUNNING...")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
