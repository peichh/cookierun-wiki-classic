import re
import os

def find_frames(plist_path):
    if not os.path.exists(plist_path):
        return
    with open(plist_path, 'r') as f:
        content = f.read()
    
    # Simple regex to find keys and their dicts containing textureRect and textureRotated
    # Look specifically for treasure_mix_frame or treasure_frame_u
    pattern = re.compile(r'<key>(treasure_mix_frame_.*?\.png|treasure_frame_u\.png)</key>\s*<dict>.*?<key>textureRect</key>\s*<string>(.*?)</string>.*?<key>textureRotated</key>\s*<(true|false)/>', re.DOTALL)
    
    print(f"--- Results from {os.path.basename(plist_path)} ---")
    for match in pattern.finditer(content):
        name = match.group(1)
        rect = match.group(2)
        rotated = match.group(3)
        print(f"Key: {name}")
        print(f"  Rect: {rect}")
        print(f"  Rotated: {rotated}")

find_frames("/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/bc_trasure_mix.plist")
find_frames("/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/bc_treasure_main.plist")
