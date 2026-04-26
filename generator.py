import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS


def safe_sample(pool, min_show=5, max_show=10):
    """biar aman kalau data kecil"""
    if not pool:
        return []

    size = min(len(pool), random.randint(min_show, max_show))
    return random.sample(pool, size)


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

        if not full_pool:
            return generate_question()

        return {
            "question": f"Sebutkan hero {role.upper()}",
            "answers": full_pool,
            "display": safe_sample(full_pool)
        }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

        full_pool = [h for h, v in HEROES.items() if lane in v["lane"]]

        if not full_pool:
            return generate_question()

        return {
            "question": f"Sebutkan hero {lane.upper()} lane",
            "answers": full_pool,
            "display": safe_sample(full_pool)
        }

    # ================= HERO REGION =================
    if q_type == "hero_region":
        regions = list(set(v["region"] for v in HEROES.values()))
        region = random.choice(regions)

        full_pool = [h for h, v in HEROES.items() if v["region"] == region]

        if not full_pool:
            return generate_question()

        return {
            "question": f"Sebutkan hero dari region {region}",
            "answers": full_pool,
            "display": safe_sample(full_pool)
        }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])

        full_pool = [i for i, v in ITEMS.items() if v["type"] == tipe]

        if not full_pool:
            return generate_question()

        return {
            "question": f"Sebutkan item {tipe.upper()}",
            "answers": full_pool,
            "display": safe_sample(full_pool)
        }

    # ================= SPELL =================
    if q_type == "spell":
        if not SPELLS:
            return generate_question()

        return {
            "question": "Sebutkan battle spell MLBB",
            "answers": SPELLS,
            "display": safe_sample(SPELLS)
        }

    return generate_question()
