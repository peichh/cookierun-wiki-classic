import sqlite3
import json
import os

def build_html():
    db_path = '/Users/peach/Documents/Poke/project/cookierun_readable_db/cookierun_classic.db'
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
    
    # 2. Prepare HTML template
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Cookie Run DB Query Simulator</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; }}
        #output {{ white-space: pre-wrap; background: #f4f4f4; padding: 10px; border: 1px solid #ccc; margin-top: 10px; max-height: 500px; overflow: auto; }}
        .controls {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>Cookie Run DB Query Simulator</h1>
    <div class="controls">
        <select id="tableSelect">
            {"".join(f'<option value="{t}">{t}</option>' for t in tables)}
        </select>
        <button onclick="queryTable()">View Table Data</button>
    </div>
    <div id="output">Select a table to view its data...</div>

    <script>
        const dbData = {json.dumps(db_snapshot)};
        
        function queryTable() {{
            const table = document.getElementById('tableSelect').value;
            const data = dbData[table];
            document.getElementById('output').textContent = JSON.stringify(data, null, 2);
        }}
    </script>
</body>
</html>
"""
    
    # 3. Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully wrote {{os.path.getsize(output_path)}} bytes to {{output_path}}")

if __name__ == "__main__":
    build_html()
