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

        if pool:
            return {
                "question": f"Sebutkan semua hero {role.upper()}",
                "answers": pool
            }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

        pool = [h for h, v in HEROES.items() if lane in v["lane"]]

        if pool:
            return {
                "question": f"Sebutkan semua hero {lane.upper()} lane",
                "answers": pool
            }

    # ================= HERO REGION =================
    if q_type == "hero_region":
        regions = list(set(v["region"] for v in HEROES.values()))
        region = random.choice(regions)

        pool = [h for h, v in HEROES.items() if v["region"] == region]

        if pool:
            return {
                "question": f"Sebutkan semua hero dari region {region}",
                "answers": pool
            }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])

        pool = [i for i, v in ITEMS.items() if v["type"] == tipe]

        if pool:
            return {
                "question": f"Sebutkan semua item {tipe.upper()}",
                "answers": pool
            }

    # ================= SPELL =================
    if q_type == "spell":
        return {
            "question": "Sebutkan semua battle spell MLBB",
            "answers": SPELLS
        }

    return generate_question()
