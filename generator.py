import random
from heroes import HEROES
from items import ITEMS, SPELLS

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
        role = random.choice(["assassin", "fighter", "mage", "tank", "marksman", "support"])
        pool = [h for h, v in HEROES.items() if v["role"] == role]

        if len(pool) >= 3:
            answers = random.sample(pool, random.randint(3, 5))
            return {
                "question": f"Sebutkan {len(answers)} hero {role.upper()}",
                "answers": answers
            }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["exp", "jungle", "mid", "gold", "roam"])
        pool = [h for h, v in HEROES.items() if v["lane"] == lane]

        if len(pool) >= 3:
            answers = random.sample(pool, random.randint(3, 5))
            return {
                "question": f"Sebutkan {len(answers)} hero {lane.upper()} lane",
                "answers": answers
            }

    # ================= HERO REGION =================
    if q_type == "hero_region":
        regions = list(set(v["region"] for v in HEROES.values()))
        region = random.choice(regions)

        pool = [h for h, v in HEROES.items() if v["region"] == region]

        if len(pool) >= 3:
            answers = random.sample(pool, random.randint(3, 5))
            return {
                "question": f"Sebutkan {len(answers)} hero dari region {region.upper()}",
                "answers": answers
            }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])
        pool = [i for i, v in ITEMS.items() if v["type"] == tipe and v.get("tier") == "full"]

        if len(pool) >= 3:
            answers = random.sample(pool, random.randint(3, 5))
            return {
                "question": f"Sebutkan {len(answers)} item {tipe.upper()}",
                "answers": answers
            }

    # ================= SPELL =================
    if q_type == "spell":
        answers = random.sample(SPELLS, random.randint(3, 5))
        return {
            "question": f"Sebutkan {len(answers)} battle spell MLBB",
            "answers": answers
        }

    # fallback kalau gagal
    return generate_question()
