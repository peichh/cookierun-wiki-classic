import os
import csv
import json
import re

EXTRACTED_DIR = "/Users/peach/Documents/cookierun file/extracted/"
OUTPUT_DIR = "/Users/peach/Documents/Poke/project/cookierun_readable_db/"

def find_all_csvs():
    csv_paths = []
    for root, dirs, files in os.walk(EXTRACTED_DIR):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(root, file))
    return csv_paths

def parse_csv(path):
    data = []
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return data

def extract_magnet_data(csv_paths):
    magnet_ranges = []
    # Look for files that might have magnetic range info
    # TreasureItemData, TreasurePassiveAttr, etc.
    for path in csv_paths:
        name = os.path.basename(path)
        if "Treasure" in name or "Cookie" in name or "Pet" in name:
            rows = parse_csv(path)
            for row in rows:
                # Common magnet keywords in CookieRun: Magnetic, Magnet, range
                for key, val in row.items():
                    if val and ("Magnet" in str(val) or "Magnetic" in str(val)):
                        magnet_ranges.append({
                            "source_file": name,
                            "id": row.get("Id") or row.get("ID") or row.get("Id_1"),
                            "name": row.get("Name") or row.get("Name_ko"),
                            "context": row
                        })
                        break
    return magnet_ranges

def extract_unit_levels(csv_paths):
    units = {"cookies": {}, "pets": {}, "treasures": {}}
    
    # Process CookieBalance, PetBalance, TreasureItemData
    for path in csv_paths:
        name = os.path.basename(path)
        rows = parse_csv(path)
        if "CookieBalance" in name:
            for row in rows:
                cid = row.get("Id") or row.get("Id_1")
                if cid: units["cookies"][cid] = row
        elif "PetBalance" in name:
            for row in rows:
                pid = row.get("Id") or row.get("Id_1")
                if pid: units["pets"][pid] = row
        elif "TreasureItemData" in name and not name.endswith("List.csv"):
            for row in rows:
                tid = row.get("Id") or row.get("Id_1")
                if tid: units["treasures"][tid] = row
                
    return units

def extract_booster_data(csv_paths):
    # Usually in PartyRunMasterConfig or similar
    for path in csv_paths:
        if "PartyRunMasterConfig" in os.path.basename(path):
            return parse_csv(path)
    return []

def main():
    print("Finding CSVs...")
    csv_paths = find_all_csvs()
    print(f"Found {len(csv_paths)} CSV files.")
    
    print("Extracting Magnet Data...")
    magnets = extract_magnet_data(csv_paths)
    with open(os.path.join(OUTPUT_DIR, "magnetic_ranges.json"), 'w') as f:
        json.dump(magnets, f, indent=2)
        
    print("Extracting Unit Levels...")
    units = extract_unit_levels(csv_paths)
    with open(os.path.join(OUTPUT_DIR, "complete_unit_levels.json"), 'w') as f:
        json.dump(units, f, indent=2)
        
    print("Extracting Booster Data...")
    boosters = extract_booster_data(csv_paths)
    with open(os.path.join(OUTPUT_DIR, "booster_data.json"), 'w') as f:
        json.dump({"boosters": boosters}, f, indent=2)
        
    print("Done. Files updated in " + OUTPUT_DIR)

if __name__ == "__main__":
    main()
