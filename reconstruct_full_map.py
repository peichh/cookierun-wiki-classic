import csv
import json
import sqlite3
import os
from pathlib import Path

LOCAL_CSV = Path("/Users/peach/Documents/cookierun file/extracted/localization_csv")
JELLY_TYPE_FILE = LOCAL_CSV / "CRXSimpleJellyTypeListData.csv"
JELLY_STAT_FILE = LOCAL_CSV / "JellyStatData.csv"
DB_FILE = "/Users/peach/Documents/Poke/project/cookierun_readable_db/database/derived_sqlite/cookierun_full_spatial.db"

def read_csv(path):
    if not path.exists(): return []
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def main():
    print("Initializing Reconstructor...")
    
    type_names = {
        "400": "House Jelly", "401": "Shield Jelly", "402": "Bonus Time", 
        "403": "Blast Jelly", "404": "Giant Jelly", "405": "Magnet Jelly",
        "406": "Coin Party", "407": "Bear Party", "408": "Small Health",
        "409": "Large Health", "500": "Basic JellyBean", "503": "Yellow Bear",
        "504": "Pink Bear", "551": "Alphabet", "552": "Coin", "553": "Gold Coin"
    }
    
    patterns = {}
    raw_patterns = read_csv(JELLY_TYPE_FILE)
    for row in raw_patterns:
        u_id = row.get("_key")
        if not u_id: continue
        slots = {}
        for k, v in row.items():
            if k.startswith("JellyTypeId_") and v and v != "0":
                try:
                    idx = int(k.split("_")[1])
                    slots[idx] = v
                except: continue
        patterns[u_id] = slots

    db_dir = os.path.dirname(DB_FILE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    if os.path.exists(DB_FILE): os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE map_entities (
            episode TEXT, stage TEXT, x INTEGER, jelly_id TEXT, name TEXT
        )
    """)

    scenarios = list(LOCAL_CSV.glob("MapStageScenario_*.csv"))
    for sf in scenarios:
        if "Shared" in sf.name: continue
        ep = sf.stem.replace("MapStageScenario_", "")
        print(f"Processing {ep}...")
        
        rows = read_csv(sf)
        for row in rows:
            stage = row.get("Stage") or row.get("ScenarioSet")
            if not stage: continue
            
            x_offset = 0
            for p_idx in range(1, 257):
                block_id = row.get(f"platform_{p_idx}")
                if block_id and block_id in patterns:
                    for slot_idx, j_id in patterns[block_id].items():
                        global_x = x_offset + slot_idx
                        cur.execute("INSERT INTO map_entities VALUES (?, ?, ?, ?, ?)",
                                   (ep, stage, global_x, j_id, type_names.get(j_id, f"ID_{j_id}")))
                
                x_offset += 256
        conn.commit()
    
    conn.close()
    print(f"Success! Database created at {DB_FILE}")

if __name__ == "__main__":
    main()