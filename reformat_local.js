const fs = require('fs');
const path = require('path');

const BASE_PATH = "/Users/peach/Documents/Poke/project/cookierun_readable_db";
const JSON_SRC = path.join(BASE_PATH, "database", "derived_json");

function loadJson(filename) {
    try {
        const fullPath = path.join(JSON_SRC, filename);
        if (!fs.existsSync(fullPath)) return [];
        return JSON.parse(fs.readFileSync(fullPath, 'utf8'));
    } catch (e) {
        return [];
    }
}

function writeMd(content, filePath) {
    const fullPath = path.join(BASE_PATH, filePath);
    const dir = path.dirname(fullPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(fullPath, content);
}

function saveCleanJson(data, filename) {
    const dir = path.join(BASE_PATH, "clean_json_api");
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, filename), JSON.stringify(data, null, 2));
}

// 1. Cookies
const cookiesRaw = loadJson("cookies_rich.json");
let cookiesMd = "# 🍪 Cookie Database\n\n| ID | Name | Grade | Unlock Condition | Max HP |\n|---|---|---|---|---|\n";
const cleanCookies = cookiesRaw.map((c) => {
    const levels = c.levels || [];
    const maxHp = levels.length > 0 ? (levels[levels.length - 1].hp || "N/A") : "N/A";
    cookiesMd += `| ${c.id} | **${c.name}** | ${c.grade} | ${c.unlock_condition} | ${maxHp} |\n`;
    return { id: c.id, name: c.name, grade: c.grade, unlock: c.unlock_condition, max_hp: maxHp };
});
writeMd(cookiesMd, "characters/cookies.md");
saveCleanJson(cleanCookies, "cookies_clean.json");

// 2. Pets
const petsRaw = loadJson("pets_rich.json");
let petsMd = "# 🐾 Pet Database\n\n| ID | Name | Grade | Unlock Condition | Behavior/Cooldown |\n|---|---|---|---|---|\n";
const cleanPets = petsRaw.map((p) => {
    const levels = p.levels || [];
    const cooldown = levels.length > 0 ? (levels[levels.length - 1].cooldown || "N/A") : "N/A";
    let extra = "";
    if (p.name === "Firefly") extra = " (Jelly ID: 4234)";
    if (p.name === "Castanets") extra = " (Jelly ID: 4338)";
    petsMd += `| ${p.id} | **${p.name}${extra}** | ${p.grade} | ${p.unlock_condition} | ${cooldown} |\n`;
    return { id: p.id, name: p.name, grade: p.grade, unlock: p.unlock_condition, max_cooldown: cooldown };
});
writeMd(petsMd, "characters/pets.md");
saveCleanJson(cleanPets, "pets_clean.json");

// 3. Treasures
const treasuresRaw = loadJson("treasures.json");
let treasuresMd = "# 💎 Treasure Registry\n\n| ID | Name | Rarity | Max Upgrade Cost (Coin) |\n|---|---|---|---|\n";
const cleanTreasures = treasuresRaw.map((t) => {
    const levels = t.levels || [];
    const maxCost = levels.length > 0 ? (levels[levels.length - 1].coin_price || "N/A") : "N/A";
    treasuresMd += `| ${t.id} | **${t.name}** | ${t.rarity} | ${maxCost} |\n`;
    return { id: t.id, name: t.name, rarity: t.rarity, max_cost: maxCost };
});
writeMd(treasuresMd, "treasures/treasures.md");
saveCleanJson(cleanTreasures, "treasures_clean.json");

// 4. Physics
const physicsMd = "# ⚙️ Physics and Formulas\n\n## Core Constants\n| Parameter | Value |\n|---|---|\n| **Gravity** | 0.8 |\n| **Jump Strength** | 14.5 |\n| **Double Jump Strength** | 12.0 |\n| **Base Health Drain** | 1 HP/sec |\n| **Max HP Cap** | 119 |\n\n## Scoring & Math\n*   Standard Jelly Score Formula: `Base + (Multiplier * Level)`\n*   Health depletion is linear unless modified by Pet/Treasure abilities.\n\n## 🏆 \"131s Set\" Farming Guide\nThe **131s Set** is optimized for high-efficiency coin/point farming.\n*   **Strategy:** Focus on maximum speed and health preservation to hit the 131-second mark in Bonus Time.\n*   **Recommended Comp:** High mobility cookies and health-extending pets.\n";
writeMd(physicsMd, "game_mechanics/physics_and_formulas.md");

// 5. Episodes
const episodesRaw = loadJson("episodes.json");
let episodesMd = "# 🗺️ Episodes and Stages\n\n| ID | Name | Total Stages | Theme |\n|---|---|---|---|\n";
episodesRaw.forEach((ep) => {
    episodesMd += `| ${ep.id || 'N/A'} | **${ep.name || 'Unknown'}** | ${ep.stages || 'N/A'} | ${ep.theme || 'N/A'} |\n`;
});
writeMd(episodesMd, "world_and_maps/episodes_and_stages.md");

console.log("Transformation Complete");
