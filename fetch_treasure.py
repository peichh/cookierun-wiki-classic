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
        
        # Look for the Treasure Name (usually in an h1 or specific title tag)
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        h1_match = re.search(r'<h1>(.*?)</h1>', html, re.IGNORECASE)
        
        # Look for stats or descriptions (broadly looking for table cells or div text)
        # This is a heuristic to capture the main content area
        main_content = re.search(r'<main.*?> (.*?) </main>', html, re.DOTALL | re.IGNORECASE)
        if not main_content:
             main_content = re.search(r'<div id="content".*?> (.*?) </div>', html, re.DOTALL | re.IGNORECASE)

        print("--- Page Title ---")
        if title_match: print(title_match.group(1).strip())
        
        print("\n--- Header (H1) ---")
        if h1_match: print(h1_match.group(1).strip())
        
        print("\n--- Raw Content Extract ---")
        # Extract plain text from the HTML body to find the treasure stats
        text = re.sub('<[^<]+?>', '', html) # Simple tag stripper
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Filter for lines that look like treasure data
        capture = False
        for line in lines:
            if "Grade" in line or "Ability" in line or "Effect" in line:
                capture = True
            if capture:
                print(line)
            if "Patch Notes" in line:
                break

except Exception as e:
    print(f"Error fetching data: {e}")
