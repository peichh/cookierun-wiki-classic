import os
import re
import xml.etree.ElementTree as ET
from PIL import Image

SOURCE_HD = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/"
TARGET_COOKIES = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/cookies_full/"
TARGET_TREASURES = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/treasure_frames/"
PUBLIC_COOKIES = "/Users/peach/Documents/Poke/project/cookierun/public/assets/cookies_full/"
PUBLIC_TREASURES = "/Users/peach/Documents/Poke/project/cookierun/public/assets/treasure_frames/"

for d in [TARGET_COOKIES, TARGET_TREASURES, PUBLIC_COOKIES, PUBLIC_TREASURES]:
    os.makedirs(d, exist_ok=True)

def parse_rect(s):
    nums = re.findall(r'\d+', s)
    return [int(n) for n in nums]

def process_plist(plist_path, img_path, filter_fn, rename_fn, target_dirs):
    if not os.path.exists(plist_path): return
    tree = ET.parse(plist_path)
    root = tree.getroot()
    
    top_dict = root.find('dict')
    keys = top_dict.findall('key')
    values = top_dict.findall('dict')
    
    frames_node = None
    for i, k in enumerate(keys):
        if k.text == 'frames':
            frames_node = values[i]
            break
            
    if frames_node is None: return
    
    f_keys = frames_node.findall('key')
    f_dicts = frames_node.findall('dict')
    
    sheet = Image.open(img_path)
    
    for i, k in enumerate(f_keys):
        name = k.text
        if not filter_fn(name): continue
        
        d = f_dicts[i]
        d_items = list(d)
        rect_str = ""
        rotated = False
        
        for j in range(len(d_items)):
            if d_items[j].tag == 'key' and d_items[j].text == 'textureRect':
                rect_str = d_items[j+1].text
            if d_items[j].tag == 'key' and d_items[j].text == 'textureRotated':
                rotated = d_items[j+1].tag == 'true'
        
        if not rect_str: continue
        x, y, w, h = parse_rect(rect_str)
        
        if rotated:
            cropped = sheet.crop((x, y, x + h, y + w)).rotate(90, expand=True)
        else:
            cropped = sheet.crop((x, y, x + w, y + h))
            
        final_name = rename_fn(name)
        for td in target_dirs:
            cropped.save(os.path.join(td, final_name))
    print(f"Finished processing {os.path.basename(plist_path)}")

# 1. Treasures
process_plist(
    os.path.join(SOURCE_HD, "bc_treasure_main.plist"),
    os.path.join(SOURCE_HD, "bc_treasure_main.png"),
    lambda n: n.startswith("treasure_frame_"),
    lambda n: n if n.endswith(".png") else f"{n}.png",
    [TARGET_TREASURES, PUBLIC_TREASURES]
)

# 2. Cookies
def cookie_rename(n):
    match = re.search(r'ch(\d+)', n)
    if match:
        cid = match.group(1)
        return f"cookie{int(cid):04d}.png"
    return n

process_plist(
    os.path.join(SOURCE_HD, "main_character.plist"),
    os.path.join(SOURCE_HD, "main_character.png"),
    lambda n: "_list" in n and "skin" not in n,
    cookie_rename,
    [TARGET_COOKIES, PUBLIC_COOKIES]
)

print("Full extraction successful.")
