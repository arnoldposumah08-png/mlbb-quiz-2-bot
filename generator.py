import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS

LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 🔥 counter global
question_counter = 0

# 🔥 anti soal kembar
recent_questions = []


def is_duplicate(q):
    return q in recent_questions


def save_question(q):
    recent_questions.append(q)
    if len(recent_questions) > 30:
        recent_questions.pop(0)


def get_valid_letter(pool):
    valid = {}

    for name in pool:
        first = name[0].upper()
        valid[first] = valid.get(first, 0) + 1

    valid_letters = [k for k, v in valid.items() if v >= 2]

    if not valid_letters:
        return random.choice(LETTERS)

    return random.choice(valid_letters)


def generate_question():
    global question_counter

    # 🔥 tiap 20 soal → 1 spell
    if question_counter >= 20:
        question_counter = 0
        return generate_spell_question()

    for _ in range(15):

        q_type = random.choice([
            "hero_role",
            "hero_lane",
            "item_type"
        ])

        # ================= HERO ROLE =================
        if q_type == "hero_role":
            role = random.choice(["Assassin", "Fighter", "Mage", "Tank", "Marksman", "Support"])

            pool = [h for h, v in HEROES.items() if role in v["role"]]
            letter = get_valid_letter(pool)

            answers = [h for h in pool if h.upper().startswith(letter)]

            if len(answers) >= 2:
                q_text = f"Sebutkan hero {role.upper()} huruf {letter}"

                if is_duplicate(q_text):
                    continue

                save_question(q_text)
                question_counter += 1

                return {
                    "question": q_text,
                    "answers": list(set(answers))
                }

        # ================= HERO LANE =================
        if q_type == "hero_lane":
            lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

            pool = [h for h, v in HEROES.items() if lane in v["lane"]]
            letter = get_valid_letter(pool)

            answers = [h for h in pool if h.upper().startswith(letter)]

            if len(answers) >= 2:
                q_text = f"Sebutkan hero {lane.upper()} huruf {letter}"

                if is_duplicate(q_text):
                    continue

                save_question(q_text)
                question_counter += 1

                return {
                    "question": q_text,
                    "answers": list(set(answers))
                }

        # ================= ITEM =================
        if q_type == "item_type":
            tipe = random.choice(["attack", "magic", "defense"])

            pool = [i for i, v in ITEMS.items() if v["type"] == tipe]
            letter = get_valid_letter(pool)

            answers = [i for i in pool if i.upper().startswith(letter)]

            if len(answers) >= 2:
                q_text = f"Sebutkan item {tipe.upper()} huruf {letter}"

                if is_duplicate(q_text):
                    continue

                save_question(q_text)
                question_counter += 1

                return {
                    "question": q_text,
                    "answers": list(set(answers))
                }

    # fallback aman
    question_counter += 1
    return {
        "question": "Sebutkan hero MLBB",
        "answers": list(HEROES.keys())
    }


# ================= SPELL =================

def generate_spell_question():

    for _ in range(10):
        letter = get_valid_letter(SPELLS)

        answers = [s for s in SPELLS if s.upper().startswith(letter)]

        if len(answers) >= 1:
            q_text = f"Sebutkan battle spell huruf {letter}"

            if is_duplicate(q_text):
                continue

            save_question(q_text)

            return {
                "question": q_text,
                "answers": list(set(answers))
            }

    return {
        "question": "Sebutkan battle spell MLBB",
        "answers": SPELLS
    }
