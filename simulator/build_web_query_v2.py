import sqlite3
import json
import os

def build_html():
    db_path = '/Users/peach/Documents/Poke/project/cookierun_readable_db/cookierun_classic.db'
    rich_cookies_path = '/Users/peach/Documents/Poke/project/cookierun/database/derived_json/cookies_rich.json'
    rich_pets_path = '/Users/peach/Documents/Poke/project/cookierun/database/derived_json/pets_rich.json'
    output_path = '/Users/peach/Documents/Poke/project/cookierun_readable_db/simulator/web_query.html'
    
    # 1. Extract data from SQLite
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    db_snapshot = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        db_snapshot[table] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()

    # 2. Enrich with JSON files if they exist
    if os.path.exists(rich_cookies_path):
        with open(rich_cookies_path, 'r') as f:
            rich_cookies = json.load(f)
            # Create a map for quick lookup
            cookie_map = {str(c['id']): c for c in rich_cookies if 'id' in c}
            for cookie in db_snapshot.get('cookies', []):
                cid = str(cookie['id'])
                if cid in cookie_map:
                    cookie['name_en'] = cookie.get('name_en') or cookie_map[cid].get('name')
                    cookie['description_en'] = cookie.get('description_en') or cookie_map[cid].get('description')

    if os.path.exists(rich_pets_path):
        with open(rich_pets_path, 'r') as f:
            rich_pets = json.load(f)
            pet_map = {str(p['id']): p for p in rich_pets if 'id' in p}
            for pet in db_snapshot.get('pets', []):
                pid = str(pet['id'])
                if pid in pet_map:
                    pet['name_en'] = pet.get('name_en') or pet_map[pid].get('name')
                    pet['description_en'] = pet.get('description_en') or pet_map[pid].get('description')

    # 3. Prepare HTML template
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Cookie Run DB Query Simulator</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; background: #fafafa; }}
        #output {{ white-space: pre-wrap; background: #fff; padding: 15px; border: 1px solid #ddd; margin-top: 10px; max-height: 600px; overflow: auto; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .controls {{ margin-bottom: 20px; display: flex; gap: 10px; align-items: center; }}
        select, button {{ padding: 8px 12px; font-size: 14px; }}
        h1 {{ color: #333; }}
        .stats {{ color: #666; font-size: 12px; margin-top: 5px; }}
    </style>
</head>
<body>
    <h1>Cookie Run DB Query Simulator</h1>
    <div class="controls">
        <select id="tableSelect">
            {"".join(f'<option value="{t}">{t}</option>' for t in tables)}
        </select>
        <button onclick="queryTable()">View Table Data</button>
        <input type="text" id="searchInput" placeholder="Search by name/id..." onkeyup="filterData()">
    </div>
    <div id="output">Select a table to view its data...</div>
    <div class="stats" id="stats"></div>

    <script>
        const dbData = {json.dumps(db_snapshot)};
        let currentTable = '';

        function queryTable() {{
            currentTable = document.getElementById('tableSelect').value;
            const data = dbData[currentTable];
            renderData(data);
        }}

        function renderData(data) {{
            document.getElementById('output').textContent = JSON.stringify(data, null, 2);
            document.getElementById('stats').textContent = `Total rows: ${{data.length}}`;
        }}

        function filterData() {{
            if (!currentTable) return;
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const filtered = dbData[currentTable].filter(item => {{
                return Object.values(item).some(val => 
                    String(val).toLowerCase().includes(searchTerm)
                );
            }});
            renderData(filtered);
        }}
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully wrote {{os.path.getsize(output_path)}} bytes to {{output_path}}")

if __name__ == "__main__":
    build_html()
