import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS

question_pool = []
used_questions = []


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
                    "question": f"Sebutkan hero {role.upper()} huruf {letter}",
                    "answers": list(set(answers))
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
                    "question": f"Sebutkan hero {lane.upper()} huruf {letter}",
                    "answers": list(set(answers))
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
                    "question": f"Sebutkan item {tipe.upper()} huruf {letter}",
                    "answers": list(set(answers))
                })

    # ================= SPELL =================
    letters = set([s[0].upper() for s in SPELLS])
    for letter in letters:
        answers = [s for s in SPELLS if s.upper().startswith(letter)]

        if len(answers) >= 1:
            pool.append({
                "question": f"Sebutkan battle spell huruf {letter}",
                "answers": list(set(answers))
            })

    return pool


def reset_pool():
    global question_pool, used_questions
    question_pool = build_question_pool()
    random.shuffle(question_pool)
    used_questions = []


def generate_question():
    global question_pool, used_questions

    if not question_pool:
        reset_pool()

    q = question_pool.pop()
    used_questions.append(q)

    return q
