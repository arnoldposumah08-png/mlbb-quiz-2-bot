import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS

LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 🔥 counter global
question_counter = 0


def generate_question():
    global question_counter

    # 🔥 setiap 11 soal → 1 spell
    if question_counter >= 10:
        question_counter = 0
        return generate_spell_question()

    # selain itu = hero/item
    for _ in range(10):
        q_type = random.choice([
            "hero_role",
            "hero_lane",
            "item_type"
        ])

        letter = random.choice(LETTERS)

        # ================= HERO ROLE =================
        if q_type == "hero_role":
            role = random.choice(["Assassin", "Fighter", "Mage", "Tank", "Marksman", "Support"])

            answers = [
                h for h, v in HEROES.items()
                if role in v["role"] and h.upper().startswith(letter)
            ]

            if len(answers) >= 2:
                question_counter += 1
                return {
                    "question": f"Sebutkan hero {role.upper()} huruf {letter}",
                    "answers": list(set(answers))
                }

        # ================= HERO LANE =================
        if q_type == "hero_lane":
            lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

            answers = [
                h for h, v in HEROES.items()
                if lane in v["lane"] and h.upper().startswith(letter)
            ]

            if len(answers) >= 2:
                question_counter += 1
                return {
                    "question": f"Sebutkan hero {lane.upper()} huruf {letter}",
                    "answers": list(set(answers))
                }

        # ================= ITEM =================
        if q_type == "item_type":
            tipe = random.choice(["attack", "magic", "defense"])

            answers = [
                i for i, v in ITEMS.items()
                if v["type"] == tipe and i.upper().startswith(letter)
            ]

            if len(answers) >= 2:
                question_counter += 1
                return {
                    "question": f"Sebutkan item {tipe.upper()} huruf {letter}",
                    "answers": list(set(answers))
                }

    # fallback kalau gagal
    question_counter += 1
    return {
        "question": "Sebutkan hero MLBB",
        "answers": list(HEROES.keys())
    }


# ================= SPELL FUNCTION =================

def generate_spell_question():
    for _ in range(10):
        letter = random.choice(LETTERS)

        answers = [
            s for s in SPELLS
            if s.upper().startswith(letter)
        ]

        if len(answers) >= 2:
            return {
                "question": f"Sebutkan battle spell huruf {letter}",
                "answers": list(set(answers))
            }

    # fallback spell
    return {
        "question": "Sebutkan battle spell MLBB",
        "answers": SPELLS
    }
