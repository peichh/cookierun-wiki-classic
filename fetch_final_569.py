import urllib.request
import re
import json

url = "https://www.cookierunhub.com/en/encyclopedia?type=treasure&id=569"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def clean_html(html):
    html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '\n', html)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        print("--- PAGE TEXT CONTENT ---")
        print(clean_html(content))
        print("\n--- DATA SCAN ---")
        # Scan raw content for "name" and "grade" nearby 569 in JSON strings
        segment = re.search(r'.{0,500}"id":\s*569.{0,1000}', content, re.DOTALL)
        if segment:
            print(f"ID 569 Data Segment: {segment.group(0)}")
        else:
            # Try searching for name patterns directly
            name_pattern = re.findall(r'"name":"(.*?)"', content)
            print(f"Names found in stream: {name_pattern[:10]}")
except Exception as e:
    print(f"Error: {e}")
