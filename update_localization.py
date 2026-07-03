import os
import json

DATABASE_ROOT = "/Users/peach/Documents/Poke/project/cookierun/database/"
DERIVED_JSON = os.path.join(DATABASE_ROOT, "derived_json")

JELLY_METADATA = {
    "4215": {
        "name_ko": "색동별파티 아이템(색동별젤리가 폭죽처럼 터지며 장애물이 부숴짐)",
        "name_en": "Colored Star Party Item: Colored Star Jellies burst like fireworks and destroy obstacles",
        "internal_id": "item12_full0",
        "internal_name": "FullScreenJellysExplotion"
    },
    "4234": {
        "name_ko": "[펫] 반딧불이가 생성하는 생명회복 질주 아이템",
        "name_en": "[Pet] Firefly's Life Recovery Blast Item",
        "internal_id": "pet42_jelly0",
        "internal_name": "FireFlyJelly"
    },
    "4338": {
        "name_ko": "[펫] 캐스터네츠가 생성하는 회복 물약",
        "name_en": "[Pet] Castanets' Recovery Potion",
        "internal_id": "item08_energy0",
        "internal_name": "CastanetsEnergyJelly"
    }
}

def update_missing_fields():
    path = os.path.join(DATABASE_ROOT, "missing_fields.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        
        if "jelly_names" in data:
            data["jelly_names"] = "Resolved for 4215, 4234, 4338. Others still checked."
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {path}")

def update_data_dictionary():
    path = os.path.join(DERIVED_JSON, "data_dictionary.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Add metadata section
        data["jelly_metadata_overrides"] = JELLY_METADATA
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {path}")

def update_jelly_data():
    # If jelly_data.json exists in root, update it
    path = os.path.join(DATABASE_ROOT, "jelly_data.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Add or update entries
        for jid, meta in JELLY_METADATA.items():
            data[jid] = meta
            
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {path}")

def update_validation_report():
    path = os.path.join(DATABASE_ROOT, "validation_report.md")
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        
        # Replace or append status
        if "## Unknown Jelly IDs Found" in content:
            new_section = "## Unknown Jelly IDs Found\n- **Resolved**: IDs 4215, 4234, 4338 have been mapped to metadata.\n"
            # Simple replacement for the example's specific pattern
            import re
            content = re.sub(r"## Unknown Jelly IDs Found.*?(?=##|$)", new_section, content, flags=re.DOTALL)
            
        with open(path, 'w') as f:
            f.write(content)
        print(f"Updated {path}")

if __name__ == "__main__":
    update_missing_fields()
    update_data_dictionary()
    update_jelly_data()
    update_validation_report()
    print("Localization update complete.")
