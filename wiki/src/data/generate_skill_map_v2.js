const fs = require('fs');
const path = require('path');

const ROOT_DB = path.join(__dirname, '../../..', 'database/derived_json');
const combiEffectsPath = path.join(ROOT_DB, 'combi_effects.json');
const cookiesRichPath = path.join(ROOT_DB, 'cookies_rich.json');
const petsRichPath = path.join(ROOT_DB, 'pets_rich.json');

const combiEffects = JSON.parse(fs.readFileSync(combiEffectsPath, 'utf8'));
const cookiesRich = JSON.parse(fs.readFileSync(cookiesRichPath, 'utf8'));
const petsRich = JSON.parse(fs.readFileSync(petsRichPath, 'utf8'));

// We need to find templates that contain variables like {0} or {1}
// Actually, in many CookieRun dumps, the descriptions are static per level
// or templates like "Revive with {0} HP"
// Let's build a map of (GID, Slot) -> Template

const templateMap = {}; 
// gid -> { slot1: "template", slot2: "template" }

combiEffects.forEach(effect => {
    const gid = effect.source_group_id;
    if (!templateMap[gid]) templateMap[gid] = {};
    
    // We try to detect if it's a template or a static string
    // In many cases, bonus_name is the "Friendly Name"
    let desc = effect.bonus_name;
    
    // Clean up "(slot 1)" suffixes
    desc = desc.replace(/\(slot \d+\)/g, '').trim();
    
    // Attempt to identify variable slots. 
    // If the value matches a number in the description, replace it with a token.
    // Example: "Revives ... with 17 HP" and value is "17" -> "Revives ... with {V1} HP"
    if (effect.bonus_value && desc.includes(effect.bonus_value)) {
        const slotToken = effect.slot === 1 ? '{V1}' : (effect.slot === 2 ? '{V2}' : '{V' + effect.slot + '}');
        // Simple replacement of the first occurrence of the exact value
        desc = desc.replace(effect.bonus_value, slotToken);
    }
    
    templateMap[gid][effect.slot] = desc;
});

const skillMap = {};
Object.keys(templateMap).forEach(gid => {
    const slots = templateMap[gid];
    // Combine slots into a coherent description
    // Priority: slot 1 is usually the main effect
    let combined = slots[1] || "";
    if (slots[2]) {
        // If slot 1 already contains {V1} and slot 2 contains {V2}, we check if they are the same sentence
        // Often slot 1 and 2 are just parts of the same template
        if (slots[1] === slots[2]) {
            combined = slots[1]; 
        } else if (slots[2].includes('{V2}') && !combined.includes('{V2}')) {
             // Heuristic: append if distinct
             combined += " " + slots[2];
        } else if (!combined.includes(slots[2])) {
             combined += " " + slots[2];
        }
    }
    skillMap[gid] = combined.trim();
});

// Manual fixes for known templates if needed
// ...

fs.writeFileSync(path.join(__dirname, 'skill_map.json'), JSON.stringify(skillMap, null, 2));

const enhancedCookies = cookiesRich.map(c => ({
    ...c,
    skill_description: skillMap[c.id] || c.skill_description || "Unique ability",
    // Ensure description_th is kept if it exists in the source
}));
fs.writeFileSync(path.join(__dirname, 'cookies_rich.json'), JSON.stringify(enhancedCookies, null, 2));

const enhancedPets = petsRich.map(p => ({
    ...p,
    skill_description: skillMap[p.id] || p.skill_description || "Pet ability"
}));
fs.writeFileSync(path.join(__dirname, 'pets_rich.json'), JSON.stringify(enhancedPets, null, 2));

console.log('Skill mapping V2 complete.');
