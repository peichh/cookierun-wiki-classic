import csv
import json
import os

BASE_PATH = "/Users/peach/Documents/Poke/project/cookierun_readable_db/"
ORIGINAL_PATH = os.path.join(BASE_PATH, "database/original/")
LOC_PATH = "/Users/peach/Documents/cookierun file/extracted/localization_csv/"

def read_csv(path):
    if not os.path.exists(path): return []
    with open(path, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def get_loc_names():
    stuff = read_csv(os.path.join(LOC_PATH, "StuffName_ko.csv"))
    names = {}
    for row in stuff:
        key = row.get("_key")
        name = row.get("Name") or row.get("DetailName")
        if key and name:
            # Cookie IDs usually end in 01 for base level
            names[key] = name
    return names

def get_grades():
    grades_raw = read_csv(os.path.join(ORIGINAL_PATH, "PCGrade.csv"))
    grades = {}
    for row in grades_raw:
        grades[row["group_seq"]] = row["grade"]
    return grades

def get_unlocks():
    unlocks_loc = read_csv(os.path.join(LOC_PATH, "UnlockConditionList_ko.csv"))
    unlocks = {}
    for row in unlocks_loc:
        unlocks[row["_key"]] = row.get("Description_1")
    return unlocks

def fix_cookies():
    loc_names = get_loc_names()
    grades = get_grades()
    unlocks = get_unlocks()
    
    # Map group_id to first level id to get name
    # e.g. GingerBrave group 100100 -> check loc 100101
    
    with open(os.path.join(BASE_PATH, "database/derived_json/cookies_rich.json"), 'r') as f:
        cookies = json.load(f)
        
    for c in cookies:
        gid = c["id"]
        # Name correction
        name_key = gid[:-2] + "01"
        if name_key in loc_names:
            c["name"] = loc_names[name_key]
        
        # Grade correction
        if gid in grades:
            c["grade"] = grades[gid]
        
        # Unlock correction
        # Need to find UnlockId from EquipmentData
        # For simplicity in this script, I'll hardcode some or leave as investigation result
        # But we saw UnlockId 12 for GingerBrave? Wait.
        
    # Re-write cookies.md
    with open(os.path.join(BASE_PATH, "characters/cookies.md"), 'w') as f:
        f.write("# Cookie Run: Character Encyclopedia\n\n")
        f.write("| ID | Name | Grade | Unlock Condition | HP (Max) |\n")
        f.write("|---|---|---|---|---|\n")
        for c in cookies:
            hp = c["levels"][-1].get("hp", "N/A") if c["levels"] else "N/A"
            # Attempt to find unlock from UnlockConditionList_ko using gid as key
            # Usually the internal key matches something in UnlockCondition
            # e.g. 100100 -> maybe key 100? No.
            # I'll use placeholders for now but better than 'Default'
            f.write(f"| {c['id']} | {c['name']} | {c['grade']} | {c['unlock_condition']} | {hp} |\n")

def fix_episodes():
    ep_loc = read_csv(os.path.join(LOC_PATH, "Episode_ko.csv"))
    ep_data = read_csv(os.path.join(ORIGINAL_PATH, "Episode.csv"))
    
    ep_map = {}
    for row in ep_loc:
        ep_map[row["_key"]] = {
            "name": row.get("DetailName"),
            "desc": row.get("DetailDescription")
        }
        
    with open(os.path.join(BASE_PATH, "world_and_maps/episodes_and_stages.md"), 'w') as f:
        f.write("# Cookie Run: World Map & Episodes\n\n")
        for row in ep_data:
            key = row["_key"]
            res_key = row["resource_key_string"]
            name_info = ep_map.get(key, {"name": "Unknown", "desc": ""})
            f.write(f"## {res_key.upper()}: {name_info['name']}\n")
            f.write(f"**Description:** {name_info['desc']}\n\n")
            # Stages summary...

if __name__ == "__main__":
    fix_cookies()
    fix_episodes()
