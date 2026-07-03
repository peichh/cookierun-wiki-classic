import os
import re
import xml.etree.ElementTree as ET
from PIL import Image

SOURCE_HD = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/"
TARGET_DIR = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/treasure_frames/"
PLIST_PATH = os.path.join(SOURCE_HD, "bc_treasure_main.plist")
PNG_PATH = os.path.join(SOURCE_HD, "bc_treasure_main.png")

def parse_rect(s):
    nums = re.findall(r'\d+', s)
    return [int(n) for n in nums]

if os.path.exists(PLIST_PATH):
    tree = ET.parse(PLIST_PATH)
    root = tree.getroot()
    main_dict = root.find('dict')
    elements = list(main_dict)
    
    frames_dict = None
    for i in range(len(elements)):
        if elements[i].tag == 'key' and elements[i].text == 'frames':
            frames_dict = elements[i+1]
            break
            
    if frames_dict is not None:
        sheet = Image.open(PNG_PATH)
        f_elements = list(frames_dict)
        
        # Search for any key containing 'masic_s' or 'magic_s'
        for i in range(0, len(f_elements), 2):
            key_name = f_elements[i].text
            if 'masic_s' in key_name or 'magic_s' in key_name:
                print(f"Found key: {key_name}")
                d = f_elements[i+1]
                d_items = list(d)
                
                rect_str = ""
                rotated = False
                for j in range(len(d_items)):
                    if d_items[j].tag == 'key' and d_items[j].text == 'textureRect':
                        rect_str = d_items[j+1].text
                    if d_items[j].tag == 'key' and d_items[j].text == 'textureRotated':
                        rotated = d_items[j+1].tag == 'true'
                
                if rect_str:
                    x, y, w, h = parse_rect(rect_str)
                    print(f"Coords: x={x}, y={y}, w={w}, h={h}, rotated={rotated}")
                    
                    if rotated:
                        cropped = sheet.crop((x, y, x + h, y + w)).rotate(90, expand=True)
                    else:
                        cropped = sheet.crop((x, y, x + w, y + h))
                    
                    # Save both versions
                    cropped.save(os.path.join(TARGET_DIR, "treasure_frame_magic_s.png"))
                    cropped.save(os.path.join(TARGET_DIR, "treasure_frame_masic_s.png"))
                    print("Files saved successfully.")
