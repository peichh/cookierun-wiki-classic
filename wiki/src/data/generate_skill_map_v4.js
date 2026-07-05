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

const skillMapEn = {};
rawSkills.forEach(row => {
    const baseId = row.id.toString();
    if (row.description_en) {
        const firstLine = row.description_en.split('\n')[0];
        const skillName = firstLine.replace(/\s+Lv\.\d+/i, '').replace(/\s+Level\s+\d+/i, '').trim();
        skillMapEn[baseId] = skillName;
    }
});

const enhancedCookies = cookiesRich.map(c => {
    const baseId = c.id.substring(0, 4);
    const skillNameEn = skillMapEn[baseId] || "Unique Skill";
    const skillNameTh = THAI_SKILL_NAMES[c.id] || skillNameEn;

    return {
        ...c,
        skill_name_en: skillNameEn,
        skill_name_th: skillNameTh
    };
});

fs.writeFileSync(path.join(__dirname, 'cookies_rich.json'), JSON.stringify(enhancedCookies, null, 2));
console.log('Skill Map Enrichment V4 Complete');
