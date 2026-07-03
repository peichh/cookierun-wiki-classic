import urllib.request
import re

url = "https://www.cookierunhub.com/en/encyclopedia?type=treasure&id=569"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        print("--- Analyzing Next.js State for Treasure 569 ---")
        
        # Extract Next.js streaming pushes
        pushes = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html)
        full_json_str = "".join(pushes).replace('\\"', '"').replace('\\\\', '\\')
        
        # Look for the specific ID 569
        if "569" in full_json_str:
            print("Found '569' in state.")
            idx = full_json_str.find("569")
            # Extract a large window around the ID to catch name and ability
            start = max(0, idx - 1000)
            end = min(len(full_json_str), idx + 2000)
            context = full_json_str[start:end]
            print(f"Captured Data Segment:\n{context}\n")
        else:
            # Check the raw HTML text as well
            text_only = re.sub('<[^<]+?>', ' ', html)
            if "569" in text_only:
                print("Found '569' in raw text.")
                idx = text_only.find("569")
                print(f"Raw Text Context:\n{text_only[idx-200:idx+800]}\n")
            else:
                print("ID 569 not found in any stream or text.")

except Exception as e:
    print(f"Error: {e}")
