import urllib.request
import json
import re

url = "https://www.cookierunhub.com/en/encyclopedia?type=treasure&id=569"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        print("--- Searching for '569' in HTML source ---")
        # Look for the ID 569 in common JSON structures or script blocks
        # Next.js often hides data in __NEXT_DATA__ or self.__next_f
        
        # 1. Find occurrences with context
        matches = re.finditer(r'.{0,100}569.{0,100}', html)
        found = False
        for i, match in enumerate(matches):
            found = True
            print(f"Match {i+1}: {match.group(0)}")
            
        if not found:
            print("No direct occurrences of '569' found in the raw HTML text.")

except Exception as e:
    print(f"Error: {e}")
