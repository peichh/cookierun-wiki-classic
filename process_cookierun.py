import os
import json
import csv
import glob
from collections import defaultdict

WORKSPACE = "/Users/peach/Documents/Poke/project/cookierun/"
DATABASE_ROOT = os.path.join(WORKSPACE, "database")
DERIVED_JSON = os.path.join(DATABASE_ROOT, "derived_json")
ORIGINAL_CSV = os.path.join(DATABASE_ROOT, "original")

def validate_maps():
    map_files = glob.glob(os.path.join(DERIVED_JSON, "map_details_*.json"))
    
    validation_results = {
        "mismatched_stage_counts": [],
        "repeated_x_values": [],
        "zero_jelly_stages": [],
        "unknown_jelly_ids": defaultdict(list)
    }
    
    known_unknown_ids = ["4215", "4234", "4338"]
    
    for mf in map_files:
        suffix = mf.split("map_details_")[-1]
        msf = os.path.join(DERIVED_JSON, f"map_spatial_details_{suffix}")
        
        if not os.path.exists(msf):
            continue
            
        with open(mf, 'r') as f:
            details = json.load(f)
        with open(msf, 'r') as f:
            spatial_list = json.load(f)
            
        details_stages = details.get("stages", [])
        
        # 1. Validate stage counts
        if len(details_stages) != len(spatial_list):
            validation_results["mismatched_stage_counts"].append(f"{suffix} (Details: {len(details_stages)}, Spatial: {len(spatial_list)})")
            
        # 2. Check jellies and x-values in spatial
        for stage_idx, stage_spatial in enumerate(spatial_list):
            jellies = stage_spatial.get("jellies", [])
            if not jellies:
                validation_results["zero_jelly_stages"].append(f"{suffix} Stage {stage_idx}")
            
            x_coords = [j.get("x") for j in jellies if "x" in j]
            if len(x_coords) != len(set(x_coords)):
                validation_results["repeated_x_values"].append(f"{suffix} Stage {stage_idx}")
                
            for j in jellies:
                jid = str(j.get("jelly_id"))
                if jid in known_unknown_ids:
                    validation_results["unknown_jelly_ids"][jid].append(f"{suffix} Stage {stage_idx}")

    return validation_results

def build_dictionaries():
    data_dict = {
        "cookies": "ultimate_cookies.json",
        "pets": "ultimate_pets.json",
        "treasures": "ultimate_treasures.json",
        "map_details": "map_details_*.json",
        "map_spatial": "map_spatial_details_*.json"
    }
    with open(os.path.join(DERIVED_JSON, "data_dictionary.json"), 'w') as f:
        json.dump(data_dict, f, indent=2)
    
    source_map = {
        "base_directory": WORKSPACE,
        "raw_assets": "database/original",
        "processed_json": "database/derived_json",
        "spatial_csv": "database/derived_csv",
        "sqlite": "database/derived_sqlite"
    }
    with open(os.path.join(DERIVED_JSON, "source_map.json"), 'w') as f:
        json.dump(source_map, f, indent=2)

def recover_unlock_links():
    recovered = {}
    if os.path.exists(ORIGINAL_CSV):
        for csv_file in glob.glob(os.path.join(ORIGINAL_CSV, "*.csv")):
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    # Sniff delimiter
                    content = f.read(1024)
                    f.seek(0)
                    dialect = csv.Sniffer().sniff(content)
                    reader = csv.DictReader(f, dialect=dialect)
                    for row in reader:
                        item_id = row.get('id') or row.get('ID')
                        unlock = row.get('unlock') or row.get('unlockCondition') or row.get('unlock_link')
                        if item_id and unlock and unlock.strip():
                            recovered[item_id] = unlock.strip()
            except:
                continue
    
    with open(os.path.join(DERIVED_JSON, "unlock_links_recovered.json"), 'w') as f:
        json.dump(recovered, f, indent=2)

def parse_ultimate_files():
    # Combi
    combi_path = os.path.join(DERIVED_JSON, "ultimate_combi_normalized.json")
    if os.path.exists(combi_path):
        with open(combi_path, 'r') as f:
            data = json.load(f)
        
        links = data.get("links", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        bonuses = data.get("bonuses", []) if isinstance(data, dict) else []
        effects = data.get("effects", []) if isinstance(data, dict) else []

        with open(os.path.join(DERIVED_JSON, "cookie_pet_combi_links.json"), 'w') as f:
            json.dump(links, f, indent=2)
        with open(os.path.join(DERIVED_JSON, "combi_bonuses.json"), 'w') as f:
            json.dump(bonuses, f, indent=2)
        with open(os.path.join(DERIVED_JSON, "combi_effects.json"), 'w') as f:
            json.dump(effects, f, indent=2)

    # Treasures
    treasure_path = os.path.join(DERIVED_JSON, "ultimate_treasures_normalized.json")
    if os.path.exists(treasure_path):
        with open(treasure_path, 'r') as f:
            data = json.load(f)
        
        candidates = data.get("effect_candidates", []) if isinstance(data, dict) else []
        t_effects = data.get("effects", []) if isinstance(data, dict) else []
        tags = data.get("tags", []) if isinstance(data, dict) else []

        with open(os.path.join(DERIVED_JSON, "treasure_effect_candidates.json"), 'w') as f:
            json.dump(candidates, f, indent=2)
        with open(os.path.join(DERIVED_JSON, "treasure_effects.json"), 'w') as f:
            json.dump(t_effects, f, indent=2)
        with open(os.path.join(DERIVED_JSON, "treasure_tags.json"), 'w') as f:
            json.dump(tags, f, indent=2)

def main():
    print("Validating maps...")
    val_report = validate_maps()
    print("Building dictionaries...")
    build_dictionaries()
    print("Recovering unlock links...")
    recover_unlock_links()
    print("Parsing ultimate files...")
    parse_ultimate_files()
    
    print("Writing reports...")
    with open(os.path.join(DATABASE_ROOT, "validation_report.md"), 'w') as f:
        f.write("# Cookie Run Database Validation Report\n\n")
        f.write("## Map Validation Summary\n")
        f.write(f"### Mismatched Stage Counts\n{', '.join(val_report['mismatched_stage_counts']) or 'None'}\n\n")
        f.write(f"### Repeated X Values\n{', '.join(val_report['repeated_x_values'][:20])}{' ...' if len(val_report['repeated_x_values']) > 20 else '' if val_report['repeated_x_values'] else 'None'}\n\n")
        f.write(f"### Zero Jelly Stages\n{', '.join(val_report['zero_jelly_stages']) or 'None'}\n\n")
        f.write(f"### Unknown Jelly IDs Found\n")
        for jid, occurrences in val_report['unknown_jelly_ids'].items():
            f.write(f"- **ID {jid}**: {len(occurrences)} occurrences\n")

    missing = {
        "jelly_names": "Localization for IDs 4215, 4234, 4338 still missing",
        "unlock_links": "Incomplete recovery from CSVs"
    }
    with open(os.path.join(DATABASE_ROOT, "missing_fields.json"), 'w') as f:
        json.dump(missing, f, indent=2)
    print("Execution Finished Successfully.")

if __name__ == "__main__":
    main()
