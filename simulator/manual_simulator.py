from __future__ import annotations

import json
import sys
import csv
import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "database" / "derived_json"

EPISODES_PATH = DERIVED / "episodes.json"
EPISODE_SCORE_PATH = DERIVED / "episode_jelly_scores_summary.json"
COOKIES_PATH = DERIVED / "cookies.json"
TREASURES_PATH = DERIVED / "treasures.json"
PETS_PATH = DERIVED / "pets.json"
BOOSTER_CODES_PATH = DERIVED / "code_explanations.json"
SPATIAL_DETAILS_TEMPLATE = DERIVED / "map_spatial_details_{episode}.json"
MECHANICS_PATH = DERIVED / "mechanics.json"
LEVEL_CONTENTS_PATH = ROOT / "database" / "original" / "LevelContents.csv"
INNER_CONFIG_PATH = ROOT / "database" / "original" / "InnerSystemConfig.csv"
COOKIE_BALANCE_PATH = ROOT / "database" / "original" / "CookieBalance.csv"
PET_BALANCE_PATH = ROOT / "database" / "original" / "PetBalance.csv"
JELLY_STAT_PATH = ROOT / "database" / "original" / "JellyStatData.csv"
TREASURE_PASSIVE_ATTR_PATH = ROOT / "database" / "original" / "TreasurePassiveAttr.csv"
TREASURE_EFFECTS_CSV = Path("/Users/peach/Documents/Cookierun data/analysis_output/human_words_db/treasure_human_effects.csv")
COLLECTION_MODEL = "distance-gated perfect X collection; Y/obstacle misses ignored"
MAP_WARNING = "current spatial map is rebuilt from 2 simple jelly patterns; coin layout is not real CRM2 map data"
# ponytail: map X is tile-ish while speed is pixel-ish; tune if real run logs disagree.
DISTANCE_SCALE = float(os.environ.get("CR_DISTANCE_SCALE", "40"))
SCORE_SCALE = float(os.environ.get("CR_SCORE_SCALE", "1"))
BASE_DRAIN = 3.0
COIN_VALUES = {"552": 1, "553": 10, "554": 5, "4117": 100}
ENERGY_VALUES = {"408": 10.0, "409": 40.0, "410": 60.0, "6014": 3.0}


@dataclass
class PickedCookie:
    id: str
    name: str
    level: int
    hp: int
    internal_key: str


@dataclass
class PickedTreasure:
    id: str
    name: str
    level: int


@dataclass
class PickedPet:
    id: str
    name: str
    level: int
    skill_value: str
    internal_key: str


@dataclass
class ScoreContext:
    player_level: int
    level_multiplier: float
    coin_multiplier: float
    applied_effects: list[str]
    unknown_effects: list[str]
    passive_attrs: list[str]


@dataclass
class MechanicsContext:
    hitboxes: dict[str, str]
    magnet_sizes: dict[str, str]
    col_areas: dict[str, str]
    magnet_jelly_range: float | None


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_level_bonus() -> dict[int, float]:
    bonuses: dict[int, float] = {}
    with LEVEL_CONTENTS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("_key") and row.get("BonusScore"):
                bonuses[int(row["_key"])] = 1.0 + (int(row["BonusScore"]) / 1000.0)
    return bonuses


def load_inner_config_values() -> dict[str, str]:
    values: dict[str, str] = {}
    with INNER_CONFIG_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) < 7:
                continue
            key = row[-1]
            if key:
                values[key] = ",".join(cell for cell in row[4:6] if cell)
    return values


def load_balance_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) >= 3 and row[-1]:
                values[row[-1]] = row[-2]
    return values


def load_magnet_jelly_range() -> float | None:
    with JELLY_STAT_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("_key") == "405" and row.get("ItemValue"):
                return int(row["ItemValue"]) / 10.0
    return None


def load_mechanics_context() -> MechanicsContext:
    inner = load_inner_config_values()
    cookies = load_balance_values(COOKIE_BALANCE_PATH)
    pets = load_balance_values(PET_BALANCE_PATH)
    return MechanicsContext(
        hitboxes={
            "Character_ColBoxSize": inner.get("Character_ColBoxSize", ""),
            "Character_ColBoxOffset": inner.get("Character_ColBoxOffset", ""),
            "Character_SlideColBoxSize": inner.get("Character_SlideColBoxSize", ""),
            "Character_SlideColBoxOffset": inner.get("Character_SlideColBoxOffset", ""),
            "Jelly_ColBoxSize": inner.get("Jelly_ColBoxSize", ""),
            "jelly_ColBoxOffset": inner.get("jelly_ColBoxOffset", ""),
        },
        magnet_sizes={
            "Baduk_MagnetSize": cookies.get("Baduk_MagnetSize", ""),
            "BariPrincess_MagnetSize": cookies.get("BariPrincess_MagnetSize", ""),
            "GARAE_TRANSFORM_MAGNET_SIZE": cookies.get("GARAE_TRANSFORM_MAGNET_SIZE", ""),
            "MallowBunny_PortalMagnetSize": cookies.get("MallowBunny_PortalMagnetSize", ""),
            "StrawberryShortcakeRunMagnetSize": cookies.get("StrawberryShortcakeRunMagnetSize", ""),
        },
        col_areas={
            "BariPrincess_SwordColArea": cookies.get("BariPrincess_SwordColArea", ""),
            "LOTUSSEED_AREA_TO_SHOOT_JELLY": pets.get("LOTUSSEED_AREA_TO_SHOOT_JELLY", ""),
        },
        magnet_jelly_range=load_magnet_jelly_range(),
    )


def level_multiplier(level: int, bonuses: dict[int, float]) -> float:
    if level in bonuses:
        return bonuses[level]
    if level <= 50:
        return 1.0 + max(level - 1, 0) / 100.0
    return 1.0 + (49.0 + (level - 50) * 0.1) / 100.0


def load_normal_episodes() -> list[dict[str, Any]]:
    episodes = load_json(EPISODES_PATH)
    score_rows = {
        row["episode"]: row
        for row in load_json(EPISODE_SCORE_PATH)
        if row.get("episode", "").startswith("epN")
    }
    rows = []
    for row in episodes:
        name = row.get("name", "")
        if not name.startswith("epN"):
            continue
        score_row = score_rows.get(name)
        if not score_row:
            continue
        rows.append(
            {
                "id": row["id"],
                "name": name,
                "base_score": int(score_row.get("estimated_base_score", 0) or 0),
                "total_jellies": int(score_row.get("total_jellies", 0) or 0),
                "collection_model": COLLECTION_MODEL,
            }
        )
    return rows


def load_spatial_stages(episode: str) -> list[dict[str, Any]]:
    path = SPATIAL_DETAILS_TEMPLATE.with_name(f"map_spatial_details_{episode}.json")
    if not path.exists():
        return []
    return load_json(path)


def load_stage_drains(episode: str) -> dict[str, float]:
    episode_num = episode.replace("epN", "").lstrip("0")
    key = f"episode_{episode_num}_stages"
    rows = load_json(MECHANICS_PATH).get(key, [])
    drains: dict[str, float] = {}
    for row in rows:
        raw = row.get("health_drain_mod")
        if raw:
            drains[str(row["stage"])] = float(raw)
    return drains


def simulate_collection(episode: dict[str, Any], starting_hp: float) -> dict[str, Any]:
    hp = starting_hp
    score = 0
    coins = 0
    jellies = 0
    reached_x = 0.0
    stages_cleared = 0
    drains = load_stage_drains(episode["name"])
    stages = load_spatial_stages(episode["name"])
    spatial_jellies = sum(len(stage.get("jellies", [])) for stage in stages)
    spatial_score = int(sum(
        int(float(jelly.get("score", 0) or 0))
        for stage in stages
        for jelly in stage.get("jellies", [])
    ))
    applied_item_effects: set[tuple[int, str]] = set()

    for stage in stages:
        start_x = float(stage["start_x"])
        end_x = float(stage["end_x"])
        x_per_second = float(stage["speed"]) / DISTANCE_SCALE
        drain = drains.get(str(stage["stage"]), BASE_DRAIN)
        current_x = start_x

        for jelly in sorted(stage.get("jellies", []), key=lambda item: int(item["x"])):
            jelly_x = float(jelly["x"])
            hp -= ((jelly_x - current_x) / x_per_second) * drain
            current_x = jelly_x
            if hp <= 0:
                return {
                    "base_score": score,
                    "base_coins": coins,
                    "collected_jellies": jellies,
                    "spatial_jellies": spatial_jellies,
                    "spatial_score": spatial_score,
                    "reached_x": round(current_x, 1),
                    "stages_cleared": stages_cleared,
                    "remaining_hp": 0.0,
                }
            jelly_id = str(jelly.get("jelly_id", ""))
            score += int(float(jelly.get("score", 0) or 0))
            coins += COIN_VALUES.get(jelly_id, 0)
            item_key = (int(jelly["x"]), jelly_id)
            if item_key not in applied_item_effects:
                hp += ENERGY_VALUES.get(jelly_id, 0.0)
                applied_item_effects.add(item_key)
            jellies += 1

        hp -= ((end_x - current_x) / x_per_second) * drain
        reached_x = end_x
        if hp <= 0:
            break
        stages_cleared += 1

    return {
        "base_score": score,
        "base_coins": coins,
        "collected_jellies": jellies,
        "spatial_jellies": spatial_jellies,
        "spatial_score": spatial_score,
        "reached_x": round(reached_x, 1),
        "stages_cleared": stages_cleared,
        "remaining_hp": round(max(hp, 0.0), 1),
    }


def load_boosters() -> dict[str, str]:
    data = load_json(BOOSTER_CODES_PATH)
    return data["pregame_boosters"]


def load_treasure_effect_rows() -> dict[str, dict[int, list[str]]]:
    if not TREASURE_EFFECTS_CSV.exists():
        return {}
    rows: dict[str, dict[int, list[str]]] = {}
    with TREASURE_EFFECTS_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            treasure_id = row.get("treasure_id", "")
            level = int(row.get("rarity_tag") or 0)
            effects = [
                value
                for key in ("effect_slot_1", "effect_slot_2", "effect_slot_3")
                for value in [row.get(key, "").strip()]
                if value and value != ":"
            ]
            rows.setdefault(treasure_id, {})[level] = effects
    return rows


def load_treasure_passive_attrs() -> dict[str, dict[int, dict[str, str]]]:
    rows: dict[str, dict[int, dict[str, str]]] = {}
    with TREASURE_PASSIVE_ATTR_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            treasure_id = row.get("group_seq", "")
            tag = row.get("tag", "")
            if treasure_id and tag.isdigit():
                rows.setdefault(treasure_id, {})[int(tag)] = row
    return rows


def parse_effect(raw: str) -> tuple[str, float] | None:
    if ":" not in raw:
        return None
    effect_id, value = raw.split(":", 1)
    try:
        return effect_id, float(value)
    except ValueError:
        return None


def build_score_context(
    player_level: int,
    treasures: list[PickedTreasure],
    treasure_rows: dict[str, dict[int, list[str]]],
    passive_rows: dict[str, dict[int, dict[str, str]]] | None = None,
) -> ScoreContext:
    applied: list[str] = []
    unknown: list[str] = []
    passive_attrs: list[str] = []
    coin_multiplier = 1.0

    for treasure in treasures:
        passive = (passive_rows or {}).get(treasure.id, {}).get(treasure.level)
        if passive:
            passive_attrs.append(
                f"{treasure.name} Lv.{treasure.level}: "
                f"{passive.get('reward')} {passive.get('method')} "
                f"prob={passive.get('prob')} qty={passive.get('qty')}"
            )
        for raw in treasure_rows.get(treasure.id, {}).get(treasure.level, []):
            parsed = parse_effect(raw)
            if not parsed:
                continue
            effect_id, value = parsed
            if effect_id == "1120":
                bonus = value / 1000.0
                coin_multiplier += bonus
                applied.append(f"{treasure.name} Lv.{treasure.level}: coin +{bonus:.3f} ({raw})")
            else:
                unknown.append(f"{treasure.name} Lv.{treasure.level}: {raw}")

    return ScoreContext(
        player_level=player_level,
        level_multiplier=level_multiplier(player_level, load_level_bonus()),
        coin_multiplier=coin_multiplier,
        applied_effects=applied,
        unknown_effects=unknown,
        passive_attrs=passive_attrs,
    )


def normalize(text: str) -> str:
    return text.strip().lower()


def find_matches(items: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    q = normalize(query)
    if not q:
        return items[:12]
    matches = []
    for item in items:
        haystacks = [str(item.get("id", "")), str(item.get("name", ""))]
        if any(q in normalize(value) for value in haystacks):
            matches.append(item)
    return matches[:12]


def choose_from_search(items: list[dict[str, Any]], label: str, allow_skip: bool = False) -> dict[str, Any] | None:
    while True:
        query = input(f"{label} search{' (blank to skip)' if allow_skip else ''}: ").strip()
        if allow_skip and not query:
            return None
        matches = find_matches(items, query)
        if not matches:
            print("No matches. Try another search.")
            continue
        for index, item in enumerate(matches, 1):
            extra = f" | HP {item['max_hp']}" if "max_hp" in item else ""
            print(f"{index}. {item['name']} [{item['id']}] {extra}")
        picked = input("Pick number: ").strip()
        if picked.isdigit() and 1 <= int(picked) <= len(matches):
            return matches[int(picked) - 1]
        print("Invalid choice.")


def choose_level(levels: list[dict[str, Any]], label: str) -> dict[str, Any]:
    non_zero = [level for level in levels if str(level.get("level", "0")) != "0"]
    max_level = int(non_zero[-1]["level"])
    while True:
        picked = input(f"{label} level (1-{max_level}): ").strip()
        if picked.isdigit():
            wanted = int(picked)
            for level in non_zero:
                if int(level["level"]) == wanted:
                    return level
        print("Invalid level.")


def load_cookies() -> list[dict[str, Any]]:
    rows = []
    for row in load_json(COOKIES_PATH):
        levels = [level for level in row.get("levels", []) if level.get("hp")]
        if not levels:
            continue
        rows.append(
            {
                "id": row["id"],
                "name": row["name"],
                "levels": levels,
                "max_hp": int(levels[-1]["hp"]),
            }
        )
    return rows


def pick_cookie(items: list[dict[str, Any]], label: str, allow_skip: bool = False) -> PickedCookie | None:
    choice = choose_from_search(items, label, allow_skip=allow_skip)
    if not choice:
        return None
    level = choose_level(choice["levels"], choice["name"])
    return PickedCookie(
        id=choice["id"],
        name=choice["name"],
        level=int(level["level"]),
        hp=int(level["hp"]),
        internal_key=level["internal_key"],
    )


def load_treasures() -> list[dict[str, Any]]:
    rows = []
    for row in load_json(TREASURES_PATH):
        rows.append(
            {
                "id": row["id"],
                "name": row["name"],
                "levels": list(range(0, len(row.get("levels", [])))),
            }
        )
    return rows


def pick_treasures(items: list[dict[str, Any]], count: int = 3) -> list[PickedTreasure]:
    picks: list[PickedTreasure] = []
    while len(picks) < count:
        print(f"Treasure slot {len(picks) + 1}/{count}")
        choice = choose_from_search(items, "Treasure", allow_skip=False)
        max_level = max(choice["levels"]) if choice["levels"] else 0
        while True:
            picked = input(f"{choice['name']} level (0-{max_level}): ").strip()
            if picked.isdigit() and int(picked) in choice["levels"]:
                picks.append(
                    PickedTreasure(
                        id=choice["id"],
                        name=choice["name"],
                        level=int(picked),
                    )
                )
                break
            print("Invalid level.")
        if len(picks) < count:
            print("Added.")
    return picks


def load_pets() -> list[dict[str, Any]]:
    rows = []
    for row in load_json(PETS_PATH):
        levels = [level for level in row.get("levels", []) if str(level.get("level", "0")) != "0"]
        if not levels:
            continue
        rows.append(
            {
                "id": row["id"],
                "name": row["name"],
                "levels": levels,
            }
        )
    return rows


def pick_pet(items: list[dict[str, Any]]) -> PickedPet:
    choice = choose_from_search(items, "Pet", allow_skip=False)
    level = choose_level(choice["levels"], choice["name"])
    return PickedPet(
        id=choice["id"],
        name=choice["name"],
        level=int(level["level"]),
        skill_value=str(level.get("skill_value", "") or ""),
        internal_key=level["internal_key"],
    )


def choose_boosters(booster_map: dict[str, str], label: str) -> list[str]:
    print(label)
    for code, name in sorted(booster_map.items(), key=lambda item: int(item[0])):
        print(f"  {code}: {name}")
    raw = input("Enter booster ids separated by commas (blank for none): ").strip()
    if not raw:
        return []
    picks = []
    for piece in raw.split(","):
        code = piece.strip()
        if code in booster_map:
            picks.append(code)
    return picks


def choose_episode(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    for index, row in enumerate(episodes, 1):
        print(f"{index}. {row['name']} | full-map base {row['base_score']:,} | jellies {row['total_jellies']:,}")
    while True:
        picked = input("Pick episode number: ").strip()
        if picked.isdigit() and 1 <= int(picked) <= len(episodes):
            return episodes[int(picked) - 1]
        print("Invalid episode.")


def choose_player_level() -> int:
    while True:
        picked = input("Player level (1-110): ").strip()
        if picked.isdigit() and 1 <= int(picked) <= 110:
            return int(picked)
        print("Invalid level.")


def effective_hp(main_cookie: PickedCookie, relay_cookie: PickedCookie | None, boosters: list[str]) -> float:
    total = float(main_cookie.hp)
    if relay_cookie:
        total += relay_cookie.hp
    if "2006" in boosters:
        total += 80.0
    if "2005" in boosters:
        total /= 0.85
    if "2012" in boosters:
        total += 20.0
    return total


def score_multiplier(boosters: list[str], random_boosts: list[str]) -> float:
    multiplier = 1.0
    for code in boosters + random_boosts:
        if code == "2004":
            multiplier *= 1.15
    return multiplier


def estimate_score(
    episode: dict[str, Any],
    main_cookie: PickedCookie,
    relay_cookie: PickedCookie | None,
    pet: PickedPet,
    treasures: list[PickedTreasure],
    boosters: list[str],
    random_boosts: list[str],
    context: ScoreContext,
) -> dict[str, Any]:
    total_hp = effective_hp(main_cookie, relay_cookie, boosters)
    collected = simulate_collection(episode, total_hp)
    base_score = float(collected["base_score"])
    total_multiplier = score_multiplier(boosters, random_boosts)
    raw_score = base_score * SCORE_SCALE * total_multiplier
    estimated = math.floor(raw_score * context.level_multiplier)
    coin_multiplier = context.coin_multiplier * (2.0 if "2003" in boosters else 1.0)
    estimated_coins = math.floor(collected["base_coins"] * coin_multiplier)
    ignored = []
    ignored.append("Y-axis misses, collisions, detailed skill spawn loops, and obstacle coin magic are ignored in MVP")
    if pet:
        ignored.append("pet effects are listed but not scored yet")
    for code in boosters + random_boosts:
        if code not in {"2004", "2005", "2006", "2012"}:
            ignored.append(f"{code} {load_boosters().get(code, 'Unknown')} not scored yet")
    return {
        "episode": episode["name"],
        "base_score": int(base_score),
        "score_scale": SCORE_SCALE,
        "full_map_score": int(episode["base_score"]),
        "scaled_base_score": math.floor(base_score * SCORE_SCALE),
        "scaled_full_map_score": math.floor(int(episode["base_score"]) * SCORE_SCALE),
        "collection_model": episode.get("collection_model", COLLECTION_MODEL),
        "map_warning": MAP_WARNING,
        "total_jellies": int(episode.get("total_jellies", 0) or 0),
        "collected_jellies": collected["collected_jellies"],
        "spatial_jellies": collected["spatial_jellies"],
        "spatial_score": collected["spatial_score"],
        "reached_x": collected["reached_x"],
        "stages_cleared": collected["stages_cleared"],
        "remaining_hp": collected["remaining_hp"],
        "effective_hp": round(total_hp, 3),
        "score_multiplier": round(total_multiplier, 3),
        "level_multiplier": round(context.level_multiplier, 3),
        "coin_multiplier": round(coin_multiplier, 3),
        "base_coins": collected["base_coins"],
        "estimated_coins": estimated_coins,
        "estimated_score": estimated,
        "applied_effects": context.applied_effects,
        "unknown_effects": context.unknown_effects,
        "passive_attrs": context.passive_attrs,
        "ignored": ignored,
    }


def print_summary(
    episode: dict[str, Any],
    main_cookie: PickedCookie,
    relay_cookie: PickedCookie | None,
    pet: PickedPet,
    treasures: list[PickedTreasure],
    boosters: list[str],
    random_boosts: list[str],
    booster_map: dict[str, str],
    context: ScoreContext,
    mechanics: MechanicsContext,
) -> None:
    result = estimate_score(episode, main_cookie, relay_cookie, pet, treasures, boosters, random_boosts, context)
    print("\nRESULT")
    print(f"Episode: {result['episode']}")
    print(f"Main: {main_cookie.name} Lv.{main_cookie.level} HP {main_cookie.hp}")
    if relay_cookie:
        print(f"Relay: {relay_cookie.name} Lv.{relay_cookie.level} HP {relay_cookie.hp}")
    else:
        print("Relay: none")
    print(f"Pet: {pet.name} Lv.{pet.level}")
    if treasures:
        print("Treasures:")
        for treasure in treasures:
            print(f"  - {treasure.name} Lv.{treasure.level}")
    else:
        print("Treasures: none")
    print("Pregame boosters:")
    if boosters:
        for code in boosters:
            print(f"  - {booster_map[code]}")
    else:
        print("  - none")
    print("Manual random boosts:")
    if random_boosts:
        for code in random_boosts:
            print(f"  - {booster_map[code]}")
    else:
        print("  - none")
    print(
        f"Collected base score: {result['base_score']:,} / spatial {result['spatial_score']:,}"
        f" / summary {result['full_map_score']:,}"
    )
    if result["score_scale"] != 1:
        print(
            f"Scaled base score: {result['scaled_base_score']:,}"
            f" / scaled summary {result['scaled_full_map_score']:,}"
        )
    print(
        f"Jellies counted: {result['collected_jellies']:,} / spatial {result['spatial_jellies']:,}"
        f" / summary {result['total_jellies']:,}"
    )
    print(f"Reached X: {result['reached_x']:,} | stages cleared: {result['stages_cleared']} | remaining HP: {result['remaining_hp']}")
    print(f"Collection model: {result['collection_model']}")
    print(f"Map warning: {result['map_warning']}")
    print(f"Effective HP: {result['effective_hp']} | distance scale: {DISTANCE_SCALE:g} | score scale: {SCORE_SCALE:g}")
    print(f"Score multiplier: {result['score_multiplier']}")
    print(f"Player level multiplier: {result['level_multiplier']} (Lv.{context.player_level})")
    print(f"Coins: {result['base_coins']:,} -> {result['estimated_coins']:,} (multiplier {result['coin_multiplier']})")
    print(f"Estimated score: {result['estimated_score']:,}")
    if result["applied_effects"]:
        print("Applied effects:")
        for line in result["applied_effects"]:
            print(f"  - {line}")
    if result["unknown_effects"]:
        print("Known but not applied yet:")
        for line in result["unknown_effects"]:
            print(f"  - {line}")
    if result["passive_attrs"]:
        print("Passive attrs found but not scored:")
        for line in result["passive_attrs"]:
            print(f"  - {line}")
    if result["ignored"]:
        print("Not scored yet:")
        for line in result["ignored"]:
            print(f"  - {line}")
    print("Mechanics constants loaded:")
    for label, values in (
        ("Hitboxes", mechanics.hitboxes),
        ("Magnet sizes", mechanics.magnet_sizes),
        ("Col areas", mechanics.col_areas),
    ):
        print(f"  {label}:")
        for key, value in values.items():
            print(f"    - {key}: {value or 'missing'}")
    if mechanics.magnet_jelly_range is not None:
        print(f"  Magnet Jelly range assumption: {mechanics.magnet_jelly_range:g} (ItemValue/10)")


def run_interactive() -> None:
    episodes = load_normal_episodes()
    cookies = load_cookies()
    pets = load_pets()
    treasures = load_treasures()
    booster_map = load_boosters()

    print("CookieRun manual simulator")
    print("normal episodes only; special episodes are excluded")
    print("MVP model: run until HP ends, then collect every listed jelly/coin up to reached X")
    player_level = choose_player_level()
    episode = choose_episode(episodes)
    main_cookie = pick_cookie(cookies, "Main cookie")
    relay_cookie = pick_cookie(cookies, "Relay cookie", allow_skip=True)
    pet = pick_pet(pets)
    picked_treasures = pick_treasures(treasures, count=3)
    boosters = choose_boosters(booster_map, "\nPregame boosters")
    random_boosts = choose_boosters(booster_map, "\nManual random boost outcomes")
    context = build_score_context(
        player_level,
        picked_treasures,
        load_treasure_effect_rows(),
        load_treasure_passive_attrs(),
    )
    print_summary(
        episode,
        main_cookie,
        relay_cookie,
        pet,
        picked_treasures,
        boosters,
        random_boosts,
        booster_map,
        context,
        load_mechanics_context(),
    )


def demo() -> None:
    episodes = load_normal_episodes()
    cookies = load_cookies()
    booster_map = load_boosters()
    assert any(row["name"] == "epN01" for row in episodes)
    main_row = next(row for row in cookies if row["name"] == "GingerBrave")
    level = next(level for level in main_row["levels"] if int(level["level"]) == 6)
    main_cookie = PickedCookie(
        id=main_row["id"],
        name=main_row["name"],
        level=6,
        hp=int(level["hp"]),
        internal_key=level["internal_key"],
    )
    result = estimate_score(
        next(row for row in episodes if row["name"] == "epN01"),
        main_cookie,
        None,
        PickedPet(id="200100", name="Choco Drop", level=1, skill_value="1000", internal_key="200101"),
        [],
        ["2004"],
        [],
        build_score_context(106, [], {}, {}),
    )
    assert result["estimated_score"] > result["base_score"]
    assert result["level_multiplier"] == 1.546
    assert result["collection_model"] == COLLECTION_MODEL
    assert booster_map["2004"] == "+15% Score Bonus"
    mechanics = load_mechanics_context()
    assert mechanics.hitboxes["Character_ColBoxSize"] == "20,52"
    assert mechanics.hitboxes["jelly_ColBoxOffset"] == "-11,-11"
    assert mechanics.magnet_sizes["BariPrincess_MagnetSize"] == "50"
    assert mechanics.magnet_jelly_range == 280.0


if __name__ == "__main__":
    demo()
    if "--demo" not in sys.argv:
        run_interactive()
