const fs = require('fs');
const path = require('path');

const ROOT_DB = path.join(__dirname, '../../..', 'database/derived_json');
const combiEffectsPath = path.join(ROOT_DB, 'combi_effects.json');
const cookiesRichPath = path.join(ROOT_DB, 'cookies_rich.json');
const petsRichPath = path.join(ROOT_DB, 'pets_rich.json');

const combiEffects = JSON.parse(fs.readFileSync(combiEffectsPath, 'utf8'));
const cookiesRich = JSON.parse(fs.readFileSync(cookiesRichPath, 'utf8'));
const petsRich = JSON.parse(fs.readFileSync(petsRichPath, 'utf8'));

// Build a map of source_group_id -> bonus_name
const bonusMap = {};
combiEffects.forEach(effect => {
    const gid = effect.source_group_id;
    if (!bonusMap[gid]) bonusMap[gid] = new Set();
    const cleanName = effect.bonus_name.replace(/\(slot \d+\)/g, '').trim();
    bonusMap[gid].add(cleanName);
});

const skillMap = {};
Object.keys(bonusMap).forEach(gid => {
    skillMap[gid] = Array.from(bonusMap[gid]).join(' ');
});

fs.writeFileSync(path.join(__dirname, 'skill_map.json'), JSON.stringify(skillMap, null, 2));

const enhancedCookies = cookiesRich.map(c => ({
    ...c,
    skill_description: skillMap[c.id] || "Unique ability"
}));
fs.writeFileSync(path.join(__dirname, 'cookies_rich.json'), JSON.stringify(enhancedCookies, null, 2));

const enhancedPets = petsRich.map(p => ({
    ...p,
    skill_description: skillMap[p.id] || "Pet ability"
}));
fs.writeFileSync(path.join(__dirname, 'pets_rich.json'), JSON.stringify(enhancedPets, null, 2));

console.log('Skill mapping and data enrichment complete.');
