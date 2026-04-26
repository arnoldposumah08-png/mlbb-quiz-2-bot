import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS


def generate_question():

    q_type = random.choice([
        "hero_role",
        "hero_lane",
        "hero_region",
        "item_type",
        "spell"
    ])

    # ================= HERO ROLE =================
    if q_type == "hero_role":
        role = random.choice(["Assassin", "Fighter", "Mage", "Tank", "Marksman", "Support"])

        full_pool = [h for h, v in HEROES.items() if role in v["role"]]

        show_pool = random.sample(full_pool, min(len(full_pool), random.randint(5, 10)))

        return {
            "question": f"Sebutkan hero {role.upper()}",
            "answers": full_pool,      # 🔥 JAWABAN BENAR = FULL KATEGORI
            "display": show_pool       # 🔥 YANG DITAMPILKAN = 5–10
        }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

        full_pool = [h for h, v in HEROES.items() if lane in v["lane"]]
        show_pool = random.sample(full_pool, min(len(full_pool), random.randint(5, 10)))

        return {
            "question": f"Sebutkan hero {lane.upper()} lane",
            "answers": full_pool,
            "display": show_pool
        }

    # ================= HERO REGION =================
    if q_type == "hero_region":
        regions = list(set(v["region"] for v in HEROES.values()))
        region = random.choice(regions)

        full_pool = [h for h, v in HEROES.items() if v["region"] == region]
        show_pool = random.sample(full_pool, min(len(full_pool), random.randint(5, 10)))

        return {
            "question": f"Sebutkan hero dari region {region}",
            "answers": full_pool,
            "display": show_pool
        }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])

        full_pool = [i for i, v in ITEMS.items() if v["type"] == tipe]
        show_pool = random.sample(full_pool, min(len(full_pool), random.randint(5, 10)))

        return {
            "question": f"Sebutkan item {tipe.upper()}",
            "answers": full_pool,
            "display": show_pool
        }

    # ================= SPELL =================
    if q_type == "spell":
        return {
            "question": "Sebutkan battle spell MLBB",
            "answers": SPELLS,
            "display": random.sample(SPELLS, min(len(SPELLS), 10))
        }

    return generate_question()
