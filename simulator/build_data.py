import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

cookies = load_json('/Users/peach/Documents/Poke/project/cookierun_readable_db/clean_json_api/cookies_clean.json')
pets = load_json('/Users/peach/Documents/Poke/project/cookierun_readable_db/clean_json_api/pets_clean.json')
treasures = load_json('/Users/peach/Documents/Poke/project/cookierun_readable_db/clean_json_api/treasures_clean.json')

# Simple mapping for sim
cookie_data = {c['name']: {'hp': int(c.get('max_hp', 160)), 'id': c['id']} for c in cookies}
pet_data = {p['name']: {'id': p['id']} for p in pets}
treasure_data = {t['name']: {'id': t['id']} for t in treasures}

# Special handling for Buttercream Choco and Golden Bar
if "Buttercream Choco Cookie" in cookie_data:
    cookie_data["Buttercream Choco Cookie"]["coin_bonus"] = 0.25

gold_bar_names = [t['name'] for t in treasures if "Golden Bar" in t['name']]
for name in gold_bar_names:
    treasure_data[name]["coin_bonus"] = 0.10 # Base estimate

combined = {
    "cookies": cookie_data,
    "pets": pet_data,
    "treasures": treasure_data
}

with open('/Users/peach/Documents/Poke/project/cookierun_readable_db/simulator/sim_data.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)
