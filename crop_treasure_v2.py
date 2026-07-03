import os
import re
from PIL import Image

plist_path = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/bc_treasure_main.plist"
image_path = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/bc_treasure_main.png"
output_dir = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/treasure_frames/"
public_dir = "/Users/peach/Documents/Poke/project/cookierun/public/assets/treasure_frames/"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(public_dir, exist_ok=True)

def parse_plist_simple(path):
    with open(path, 'r') as f:
        content = f.read()
    
    frames = {}
    # Find each key and its corresponding textureRect and textureRotated
    pattern = re.compile(r'<key>(treasure_frame_.*?\.png)</key>\s*<dict>.*?<key>textureRect</key>\s*<string>\{\{(.*?),(.*?)\},\{(.*?),(.*?)\}\}</string>.*?<key>textureRotated</key>\s*<(true|false)/>', re.DOTALL)
    
    for match in pattern.finditer(content):
        name = match.group(1).replace('.png', '')
        x, y, w, h = int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5))
        rotated = match.group(6) == 'true'
        frames[name] = {'rect': (x, y, w, h), 'rotated': rotated}
    return frames

frames_to_extract = [
    'treasure_frame_c', 'treasure_frame_b', 'treasure_frame_a', 
    'treasure_frame_s', 'treasure_frame_ss', 'treasure_frame_l', 
    'treasure_frame_masic_s'
]

sheet = Image.open(image_path)
data = parse_plist_simple(plist_path)

print("Parsed coordinates:")
for name in frames_to_extract:
    if name in data:
        item = data[name]
        x, y, w, h = item['rect']
        rotated = item['rotated']
        print(f"{name}: rect=({x}, {y}, {w}, {h}), rotated={rotated}")
        
        # PIL crop box is (left, top, right, bottom)
        if rotated:
            crop_box = (x, y, x + h, y + w)
            cropped = sheet.crop(crop_box).rotate(90, expand=True)
        else:
            crop_box = (x, y, x + w, y + h)
            cropped = sheet.crop(crop_box)
            
        cropped.save(os.path.join(output_dir, f"{name}.png"))
        cropped.save(os.path.join(public_dir, f"{name}.png"))
    else:
        print(f"Warning: {name} not found in plist")

print("Cropping done.")
