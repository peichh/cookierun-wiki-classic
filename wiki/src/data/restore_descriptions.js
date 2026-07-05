const fs = require('fs');
const path = require('path');

const currentPath = path.join(__dirname, 'cookies_rich.json');
const backupPath = path.join(__dirname, 'cookies_rich_backup.json');

const current = JSON.parse(fs.readFileSync(currentPath, 'utf8'));
const backup = JSON.parse(fs.readFileSync(backupPath, 'utf8'));

const backupMap = {};
backup.forEach(c => {
    backupMap[c.id] = {
        desc_en: c.skill_description_en,
        desc_th: c.skill_description_th
    };
});

const restored = current.map(c => {
    const b = backupMap[c.id];
    return {
        ...c,
        skill_description_en: b ? b.desc_en : (c.skill_description_en || "Unique skill"),
        skill_description_th: b ? b.desc_th : (c.skill_description_th || "ความสามารถพิเศษ")
    };
});

fs.writeFileSync(currentPath, JSON.stringify(restored, null, 2));
console.log('Descriptions Restored from Backup');
