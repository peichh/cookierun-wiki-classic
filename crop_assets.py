import os
from PIL import Image

# Directories
SOURCE_DIR = "/Users/peach/Documents/cookierun file/extracted/apk/base/assets/kakaoBC_HD/"
TARGET_COOKIES = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/cookies_full/"
TARGET_TREASURES = "/Users/peach/Documents/Poke/project/cookierun_readable_db/assets/treasure_frames/"
PUBLIC_COOKIES = "/Users/peach/Documents/Poke/project/cookierun/public/assets/cookies_full/"
PUBLIC_TREASURES = "/Users/peach/Documents/Poke/project/cookierun/public/assets/treasure_frames/"

os.makedirs(TARGET_COOKIES, exist_ok=True)
os.makedirs(TARGET_TREASURES, exist_ok=True)
os.makedirs(PUBLIC_COOKIES, exist_ok=True)
os.makedirs(PUBLIC_TREASURES, exist_ok=True)

# 1. Copy Cookies (Lobby Illustrations)
for i in range(1, 100):
    name = f"ch{i:02d}.png"
    src = os.path.join(SOURCE_DIR, name)
    if os.path.exists(src):
        img = Image.open(src)
        img.save(os.path.join(TARGET_COOKIES, name))
        img.save(os.path.join(PUBLIC_COOKIES, name))

# 2. Crop Treasure Frames from bc_treasure_main.png
# Manual coordinates for HD frames (Standard sizes found in .plist)
# These are approximations for C, B, A, S, SS, L frames
frames = {
    "treasure_frame_c": (2, 2, 102, 102),
    "treasure_frame_b": (106, 2, 206, 102),
    "treasure_frame_a": (210, 2, 310, 102),
    "treasure_frame_s": (314, 2, 414, 102),
    "treasure_frame_ss": (418, 2, 518, 102),
    "treasure_frame_l": (522, 2, 622, 102),
    "treasure_frame_magic_s": (626, 2, 726, 102)
}

treasure_sheet = os.path.join(SOURCE_DIR, "bc_treasure_main.png")
if os.path.exists(treasure_sheet):
    sheet = Image.open(treasure_sheet)
    for name, box in frames.items():
        cropped = sheet.crop(box)
        cropped.save(os.path.join(TARGET_TREASURES, f"{name}.png"))
        cropped.save(os.path.join(PUBLIC_TREASURES, f"{name}.png"))

print("Asset cropping and copying complete.")
