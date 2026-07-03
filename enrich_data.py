import os
import json
import csv
import glob

WORKSPACE = "/Users/peach/Documents/Poke/project/cookierun/"
ORIGINAL_CSV = os.path.join(WORKSPACE, "database/original")
DERIVED_JSON = os.path.join(WORKSPACE, "database/derived_json")

if not os.path.exists(DERIVED_JSON):
    os.makedirs(DERIVED_JSON)

def load_csv(filename):
    path = os.path.join(ORIGINAL_CSV, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def enrich_unlocks():
    print("Enriching Unlocks...")
    unlocks_raw = load_csv('UnlockCondition.csv')
    enriched = []
    for row in unlocks_raw:
        enriched.append({
            "id": row.get('_key'),
            "conditions": [
                {
                    "type_id": row.get(f'ConditionId_{i}'),
                    "param": row.get(f'Parameter_{i}'),
                    "amount": row.get(f'RequiredAmount_{i}')
                } for i in range(1, 4) if row.get(f'ConditionId_{i}') != '0'
            ]
        })
    with open(os.path.join(DERIVED_JSON, "cookie_pet_unlocks.json"), 'w') as f:
        json.dump(enriched, f, indent=2)
    return len(enriched)

def enrich_combi():
    print("Enriching Combi Bonus...")
    ultimate_combi_path = os.path.join(DERIVED_JSON, "ultimate_combi.json")
    links = []
    if os.path.exists(ultimate_combi_path):
        with open(ultimate_combi_path, 'r') as f:
            data = json.load(f)
        if isinstance(data, list):
            links = data
        elif isinstance(data, dict):
            links = data.get("links", data.get("combi", []))
    
    with open(os.path.join(DERIVED_JSON, "cookie_pet_combi_links.json"), 'w') as f:
        json.dump(links, f, indent=2)
    return len(links)

def enrich_treasures():
    print("Enriching Treasures...")
    treasures_raw = load_csv('TreasureItemData.csv')
    passive_attr = {row['group_seq']: row for row in load_csv('TreasurePassiveAttr.csv') if row.get('tag') == '0'}
    
    enriched = []
    for row in treasures_raw:
        tid = row.get('group_seq')
        item = {
            "id": tid,
            "level": row.get('tag'),
            "name": row.get('stuff_name'),
            "price_coin": row.get('priceA'),
            "price_crystal": row.get('priceB'),
            "type": row.get('stuffType')
        }
        if tid in passive_attr:
            item["effect_type"] = passive_attr[tid].get('reward')
            item["base_amount"] = passive_attr[tid].get('qty')
            
        enriched.append(item)
    with open(os.path.join(DERIVED_JSON, "treasure_effects.json"), 'w') as f:
        json.dump(enriched, f, indent=2)
    return len(enriched)

def deep_source_map():
    print("Generating Deep Source Map...")
    csv_files = glob.glob(os.path.join(ORIGINAL_CSV, "*.csv"))
    json_files = glob.glob(os.path.join(DERIVED_JSON, "*.json"))
    source_map = {
        "raw_csv_stats": [{"file": os.path.basename(f), "size_kb": os.path.getsize(f)//1024} for f in csv_files],
        "derived_json_stats": [{"file": os.path.basename(f), "size_kb": os.path.getsize(f)//1024} for f in json_files],
        "mapping": {
            "UnlockCondition.csv": "cookie_pet_unlocks.json",
            "TreasureItemData.csv": "treasure_effects.json",
            "TreasurePassiveAttr.csv": "treasure_effects.json"
        }
    }
    with open(os.path.join(DERIVED_JSON, "source_map.json"), 'w') as f:
        json.dump(source_map, f, indent=2)

def expand_dictionary():
    print("Expanding Data Dictionary...")
    data_dictionary = {
        "cookie_pet_unlocks": {
            "description": "Normalized unlock requirements extracted from UnlockCondition.csv.",
            "fields": {
                "id": "Internal ID of cookie or pet",
                "conditions": "Array of requirements (ConditionId, Param, Amount)"
            }
        },
        "treasure_effects": {
            "description": "Enriched treasure data combining items and passive attributes.",
            "fields": {
                "id": "Treasure group ID",
                "level": "Upgrade stage (0-10)",
                "effect_type": "The internal code for the reward/effect",
                "base_amount": "The base value of the effect"
            }
        },
        "cookie_pet_combi_links": {
            "description": "Mapping of synergy bonuses between cookies and pets."
        }
    }
    with open(os.path.join(DERIVED_JSON, "data_dictionary.json"), 'w') as f:
        json.dump(data_dictionary, f, indent=2)

def main():
    u_count = enrich_unlocks()
    c_count = enrich_combi()
    t_count = enrich_treasures()
    deep_source_map()
    expand_dictionary()
    print(f"Summary: {u_count} unlocks, {c_count} combis, {t_count} treasure records.")

if __name__ == "__main__":
    main()
