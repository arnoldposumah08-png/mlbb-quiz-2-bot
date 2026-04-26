import random
from heroes import HEROES
from items import ITEMS
from spells import SPELLS


def safe_sample(pool, min_show=5, max_show=10):
    if not pool:
        return []

    size = min(len(pool), random.randint(min_show, max_show))
    return random.sample(pool, size)


def pick_question():

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

        if full_pool:
            return {
                "question": f"Sebutkan hero {role.upper()}",
                "answers": full_pool,
                "display": safe_sample(full_pool)
            }

    # ================= HERO LANE =================
    if q_type == "hero_lane":
        lane = random.choice(["EXP", "Jungle", "Mid", "Gold", "Roam"])

        full_pool = [h for h, v in HEROES.items() if lane in v["lane"]]

        if full_pool:
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

        if full_pool:
            return {
                "question": f"Sebutkan hero dari region {region}",
                "answers": full_pool,
                "display": safe_sample(full_pool)
            }

    # ================= ITEM =================
    if q_type == "item_type":
        tipe = random.choice(["attack", "magic", "defense"])

        full_pool = [i for i, v in ITEMS.items() if v["type"] == tipe]

        if full_pool:
            return {
                "question": f"Sebutkan item {tipe.upper()}",
                "answers": full_pool,
                "display": safe_sample(full_pool)
            }

    # ================= SPELL =================
    if q_type == "spell":
        if SPELLS:
            return {
                "question": "Sebutkan battle spell MLBB",
                "answers": SPELLS,
                "display": safe_sample(SPELLS)
            }

    # ❗ FALLBACK AMAN (NO RECURSION)
    # instead of generate_question() recursion (danger)
    return {
        "question": "Sebutkan battle spell MLBB",
        "answers": SPELLS,
        "display": safe_sample(SPELLS)
    }


def generate_question():
    return pick_question()
