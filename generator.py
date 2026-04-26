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
        pool = [h for h, v in HEROES.items() if role in v["role"]]

        limit = min(len(pool), random.randint(5, 10))
        answers = random.sample(pool, limit)

        return {
            "question": f"Sebutkan {limit} hero {role.upper()}",
            "answers": answers,
            "mode": "role",
            "key": role
        }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])
        pool = [h for h, v in HEROES.items() if lane in v["lane"]]

        limit = min(len(pool), random.randint(5, 10))
        answers = random.sample(pool, limit)

        return {
            "question": f"Sebutkan {limit} hero {lane.upper()} lane",
            "answers": answers,
            "mode": "lane",
            "key": lane
        }

    # ================= HERO REGION =================
    if q_type == "hero_region":
        regions = list(set(v["region"] for v in HEROES.values()))
        region = random.choice(regions)
        pool = [h for h, v in HEROES.items() if v["region"] == region]

        limit = min(len(pool), random.randint(5, 10))
        answers = random.sample(pool, limit)

        return {
            "question": f"Sebutkan {limit} hero dari region {region}",
            "answers": answers,
            "mode": "region",
            "key": region
        }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])
        pool = [i for i, v in ITEMS.items() if v["type"] == tipe]

        limit = min(len(pool), random.randint(5, 10))
        answers = random.sample(pool, limit)

        return {
            "question": f"Sebutkan {limit} item {tipe.upper()}",
            "answers": answers,
            "mode": "item",
            "key": tipe
        }

    # ================= SPELL =================
    if q_type == "spell":
        limit = min(len(SPELLS), random.randint(5, 10))
        answers = random.sample(SPELLS, limit)

        return {
            "question": f"Sebutkan {limit} battle spell MLBB",
            "answers": answers,
            "mode": "spell",
            "key": "spell"
        }

    return generate_question()
