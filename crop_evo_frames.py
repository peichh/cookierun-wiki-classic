import os
from PIL import Image

# Configuration
SOURCE_PNG = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/bc_treasure_main.png"
TARGET_DIR = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/treasure_frames/"

# Metadata found in previous step
frames = {
    "treasure_frame_u.png": (650, 767, 126, 126),
    "treasure_mix_frame_l.png": (650, 895, 126, 126),
    "treasure_mix_frame_ss.png": (521, 1023, 126, 126),
    "treasure_mix_frame_s.png": (778, 895, 126, 126),
    "treasure_mix_frame_a.png": (778, 767, 126, 126),
    "treasure_mix_frame_b.png": (522, 895, 126, 126),
    "treasure_mix_frame_c.png": (352, 956, 126, 126)
}

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

sheet = Image.open(SOURCE_PNG)

print("--- Cropping Evolved Treasure Frames ---")
for name, (x, y, w, h) in frames.items():
    # PIL crop is (left, top, right, bottom)
    crop_box = (x, y, x + w, y + h)
    cropped = sheet.crop(crop_box)
    
    save_path = os.path.join(TARGET_DIR, name)
    cropped.save(save_path)
    print(f"Saved: {name} | Size: {cropped.size}")

print("--- Done ---")
