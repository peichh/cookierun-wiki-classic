import os
import re

BASE_PATH = "/Users/peach/Documents/Poke/project/cookierun_readable_db/"

# Update Cookies
cookie_md = os.path.join(BASE_PATH, "characters/cookies.md")
if os.path.exists(cookie_md):
    with open(cookie_md, 'r') as f:
        content = f.read()
    
    # Replace the old guessed chXX.png with cookie00XX.png
    def replace_cookie_img(match):
        prefix = match.group(1) # ID like 100100
        cid = prefix[2:4] # 01
        return f"| {prefix} | **{match.group(2)}** <br> ![{match.group(2)}](/assets/cookies_full/cookie00{cid}.png) |"

    # Pattern to match the row up to the Name/Image part
    new_content = re.sub(r'\| (10\d{4}) \| \*\*(.*?)\*\* <br> !\[.*?\]\(.*?\)\s*\|', replace_cookie_img, content)
    with open(cookie_md, 'w') as f:
        f.write(new_content)

# Update Treasures
treasure_md = os.path.join(BASE_PATH, "treasures/treasures.md")
if os.path.exists(treasure_md):
    with open(treasure_md, 'r') as f:
        content = f.read()
    
    # Verify the frames are correctly linked
    # We already used /assets/treasure_frames/treasure_frame_c.png etc in the previous step
    # but let's make sure it's the right naming
    content = content.replace("treasure_frame_masic_s.png", "treasure_frame_masic_s.png") # no change needed
    with open(treasure_md, 'w') as f:
        f.write(content)

print("DB image links updated.")
