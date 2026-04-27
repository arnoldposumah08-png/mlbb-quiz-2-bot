import random
import database
from heroes import HEROES
from items import ITEMS
from spells import SPELLS

# ================= BUILD QUESTIONS =================

def build_question_pool():
    pool = []

    # ================= HERO ROLE =================
    roles = ["Assassin", "Fighter", "Mage", "Tank", "Marksman", "Support"]
    for role in roles:
        heroes = [h for h, v in HEROES.items() if role in v["role"]]

        letters = set([h[0].upper() for h in heroes])

        for letter in letters:
            answers = [h for h in heroes if h.upper().startswith(letter)]

            if len(answers) >= 2:
                pool.append({
                    "category": "hero",
                    "question": f"Sebutkan hero {role.upper()} huruf {letter}",
                    "answers": sorted(list(set(answers)))
                })

    # ================= HERO LANE =================
    lanes = ["EXP", "Jungle", "Mid", "Gold", "Roam"]
    for lane in lanes:
        heroes = [h for h, v in HEROES.items() if lane in v["lane"]]

        letters = set([h[0].upper() for h in heroes])

        for letter in letters:
            answers = [h for h in heroes if h.upper().startswith(letter)]

            if len(answers) >= 2:
                pool.append({
                    "category": "hero",
                    "question": f"Sebutkan hero {lane.upper()} huruf {letter}",
                    "answers": sorted(list(set(answers)))
                })

    # ================= ITEM =================
    types = ["attack", "magic", "defense"]
    for tipe in types:
        items = [i for i, v in ITEMS.items() if v["type"] == tipe]

        letters = set([i[0].upper() for i in items])

        for letter in letters:
            answers = [i for i in items if i.upper().startswith(letter)]

            if len(answers) >= 2:
                pool.append({
                    "category": "item",
                    "question": f"Sebutkan item {tipe.upper()} huruf {letter}",
                    "answers": sorted(list(set(answers)))
                })

    # ================= SPELL =================
    letters = set([s[0].upper() for s in SPELLS])
    for letter in letters:
        answers = [s for s in SPELLS if s.upper().startswith(letter)]

        if len(answers) >= 1:
            pool.append({
                "category": "spell",
                "question": f"Sebutkan battle spell huruf {letter}",
                "answers": sorted(list(set(answers)))
            })

    return pool


# ================= AUTO GENERATE + INSERT =================

def generate_question():
    """
    Ambil soal dari database.
    Jika kosong → generate otomatis → simpan → ambil lagi
    """

    # 🔥 pastikan DB siap
    database.init_db()

    # ambil dari DB
    q = database.get_random_question()

    if q and q.get("answers"):
        return q

    print("⚠️ Database kosong, generate soal otomatis...")

    # generate semua soal
    pool = build_question_pool()

    if not pool:
        return {
            "question": "❌ Gagal generate soal (pool kosong)!",
            "answers": []
        }

    for item in pool:
        try:
            database.insert_question(
                item["category"],
                item["question"],
                item["answers"]
            )
        except Exception as e:
            # amanin biar gak crash
            print("INSERT ERROR:", e)

    print(f"✅ {len(pool)} soal berhasil dibuat")

    # ambil lagi setelah isi
    q = database.get_random_question()

    if not q:
        return {
            "question": "❌ Gagal ambil soal setelah generate!",
            "answers": []
        }

    return q
    
    def clear_questions():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM questions")

    conn.commit()
    cur.close()
    conn.close()


# ================= OPTIONAL MANUAL RUN =================

def insert_all_to_db():
    database.init_db()

    pool = build_question_pool()

    if not pool:
        print("❌ Pool kosong!")
        return

    for q in pool:
        try:
            database.insert_question(
                q["category"],
                q["question"],
                q["answers"]
            )
        except Exception as e:
            print("INSERT ERROR:", e)

    print(f"✅ {len(pool)} soal berhasil diproses (tanpa duplikat)")


# ================= RUN =================

if __name__ == "__main__":
    insert_all_to_db()
