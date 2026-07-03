import os
import re
from PIL import Image

# Configuration
SOURCE_HD = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/"
TARGET_COOKIES = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/cookies_full/"
TARGET_TREASURES = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/treasure_frames/"
PUBLIC_COOKIES = "/Users/peach/Documents/Poke/project/cookierun/public/assets/cookies_full/"
PUBLIC_TREASURES = "/Users/peach/Documents/Poke/project/cookierun/public/assets/treasure_frames/"

os.makedirs(TARGET_COOKIES, exist_ok=True)
os.makedirs(TARGET_TREASURES, exist_ok=True)
os.makedirs(PUBLIC_COOKIES, exist_ok=True)
os.makedirs(PUBLIC_TREASURES, exist_ok=True)

def parse_plist(path):
    with open(path, 'r') as f:
        content = f.read()
    frames = {}
    pattern = re.compile(r'<key>(.*?\.png)</key>\s*<dict>.*?<key>textureRect</key>\s*<string>\{\{(.*?),(.*?)\},\{(.*?),(.*?)\}\}</string>.*?<key>textureRotated</key>\s*<(true|false)/>', re.DOTALL)
    for match in pattern.finditer(content):
        name = match.group(1).replace('.png', '')
        x, y, w, h = int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5))
        rotated = match.group(6) == 'true'
        frames[name] = {'rect': (x, y, w, h), 'rotated': rotated}
    return frames

# 1. Extract Treasure Frames
treasure_plist = os.path.join(SOURCE_HD, "bc_treasure_main.plist")
treasure_image = os.path.join(SOURCE_HD, "bc_treasure_main.png")
if os.path.exists(treasure_plist) and os.path.exists(treasure_image):
    sheet = Image.open(treasure_image)
    data = parse_plist(treasure_plist)
    frames = ['treasure_frame_c', 'treasure_frame_b', 'treasure_frame_a', 'treasure_frame_s', 'treasure_frame_ss', 'treasure_frame_l', 'treasure_frame_masic_s']
    for name in frames:
        if name in data:
            item = data[name]
            x, y, w, h = item['rect']
            rotated = item['rotated']
            if rotated:
                cropped = sheet.crop((x, y, x + h, y + w)).rotate(90, expand=True)
            else:
                cropped = sheet.crop((x, y, x + w, y + h))
            cropped.save(os.path.join(TARGET_TREASURES, f"{name}.png"))
            cropped.save(os.path.join(PUBLIC_TREASURES, f"{name}.png"))

# 2. Extract Cookie List Icons (Since full body standing is hard to find, use high-res list icons)
cookie_plist = os.path.join(SOURCE_HD, "main_character.plist")
cookie_image = os.path.join(SOURCE_HD, "main_character.png")
if os.path.exists(cookie_plist) and os.path.exists(cookie_image):
    sheet = Image.open(cookie_image)
    data = parse_plist(cookie_plist)
    for name, item in data.items():
        if "_list" in name and "skin" not in name:
            x, y, w, h = item['rect']
            rotated = item['rotated']
            if rotated:
                cropped = sheet.crop((x, y, x + h, y + w)).rotate(90, expand=True)
            else:
                cropped = sheet.crop((x, y, x + w, y + h))
            # Rename ch01_list to cookie0001.png etc
            cookie_id = name.split('_')[0].replace('ch', '')
            final_name = f"cookie{int(cookie_id):04d}.png"
            cropped.save(os.path.join(TARGET_COOKIES, final_name))
            cropped.save(os.path.join(PUBLIC_COOKIES, final_name))

print("Extraction complete.")
