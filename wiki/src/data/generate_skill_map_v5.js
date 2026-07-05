const fs = require('fs');
const path = require('path');

const ROOT_DB_JSON = path.join(__dirname, '../../..', 'database/derived_json');
const cookiesRichPath = path.join(ROOT_DB_JSON, 'cookies_rich.json');
const rawSkillsPath = path.join(__dirname, 'cookie_skills_raw.json');

const cookiesRich = JSON.parse(fs.readFileSync(cookiesRichPath, 'utf8'));
const rawSkills = JSON.parse(fs.readFileSync(rawSkillsPath, 'utf8'));

const THAI_SKILL_NAMES = {
    "108200": "สลัดบอมบ์",
    "101300": "คืนชีพซอมบี้",
    "100500": "เรียกปาร์ตี้พลุเหรียญ",
    "100200": "โบนัสไทม์สตรอว์เบอร์รี่"
};

const skillMap = {};
rawSkills.forEach(row => {
    const baseId = row.id.toString();
    if (row.description_en) {
        const lines = row.description_en.split('\n');
        const firstLine = lines[0];
        const skillName = firstLine.replace(/\s+Lv\.\d+/i, '').replace(/\s+Level\s+\d+/i, '').trim();
        
        // Full description is everything after the first line
        const fullDesc = lines.slice(1).join('\n').trim();
        
        skillMap[baseId] = {
            name: skillName,
            description: fullDesc
        };
    }
});

const enhancedCookies = cookiesRich.map(c => {
    const baseId = c.id.substring(0, 4);
    const dbData = skillMap[baseId] || { name: "Unique Skill", description: "" };
    
    const skillNameEn = dbData.name;
    const skillNameTh = THAI_SKILL_NAMES[c.id] || skillNameEn;
    
    // We want to keep the skill descriptions!
    // Since we don't have a Thai description database, we fallback to English
    const skillDescriptionEn = dbData.description || "Unique skill";
    const skillDescriptionTh = skillDescriptionEn; // Fallback or use manual mapping if we had it

    return {
        ...c,
        skill_name_en: skillNameEn,
        skill_name_th: skillNameTh,
        skill_description_en: skillDescriptionEn,
        skill_description_th: skillDescriptionTh
    };
});

fs.writeFileSync(path.join(__dirname, 'cookies_rich.json'), JSON.stringify(enhancedCookies, null, 2));
console.log('Skill Map Enrichment V5 Complete - Descriptions Preserved (vía SQLite mapping)');
