import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS

LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def generate_question():

    q_type = random.choice([
        "hero_role",
        "hero_lane",
        "item_type",
        "spell"
    ])

    letter = random.choice(LETTERS)

    # ================= HERO ROLE =================
    if q_type == "hero_role":
        role = random.choice(["Assassin", "Fighter", "Mage", "Tank", "Marksman", "Support"])

        answers = [
            h for h, v in HEROES.items()
            if role in v["role"] and h.upper().startswith(letter)
        ]

        if answers:
            return {
                "question": f"Sebutkan hero {role.upper()} huruf {letter}",
                "answers": answers
            }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

        answers = [
            h for h, v in HEROES.items()
            if lane in v["lane"] and h.upper().startswith(letter)
        ]

        if answers:
            return {
                "question": f"Sebutkan hero {lane.upper()} huruf {letter}",
                "answers": answers
            }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])

        answers = [
            i for i, v in ITEMS.items()
            if v["type"] == tipe and i.upper().startswith(letter)
        ]

        if answers:
            return {
                "question": f"Sebutkan item {tipe.upper()} huruf {letter}",
                "answers": answers
            }

    # ================= SPELL =================
    if q_type == "spell":

        answers = [
            s for s in SPELLS
            if s.upper().startswith(letter)
        ]

        if answers:
            return {
                "question": f"Sebutkan battle spell huruf {letter}",
                "answers": answers
            }

    # fallback biar tidak kosong
    return {
        "question": "Sebutkan battle spell MLBB",
        "answers": SPELLS
    }
