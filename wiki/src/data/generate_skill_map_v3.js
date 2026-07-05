const fs = require('fs');
const path = require('path');

const ROOT_DB = path.join(__dirname, '../../..', 'database/derived_json');
const combiEffects = JSON.parse(fs.readFileSync(path.join(ROOT_DB, 'combi_effects.json'), 'utf8'));
const cookiesRich = JSON.parse(fs.readFileSync(path.join(ROOT_DB, 'cookies_rich.json'), 'utf8'));
const petsRich = JSON.parse(fs.readFileSync(path.join(ROOT_DB, 'pets_rich.json'), 'utf8'));

// Extract detailed descriptions
const skillMap = {};
combiEffects.forEach(effect => {
    const gid = effect.source_group_id;
    if (!skillMap[gid]) skillMap[gid] = new Set();
    let desc = effect.bonus_name.replace(/\(slot \d+\)/g, '').trim();
    skillMap[gid].add(desc);
});

const finalizedSkills = {};
Object.keys(skillMap).forEach(gid => {
    finalizedSkills[gid] = Array.from(skillMap[gid]).join(' ');
});

// Enriched Thai Mechanics Mapping
const THAI_MECHANICS = {
    "108200": "เมื่อเกจเต็ม คุกกี้สลัดมันฝรั่งจะขี่มอเตอร์ไซค์ส่งของ โดยจะมีมันฝรั่งต้มและมายองเนสกระจายเต็มพื้น การขี่ผ่านสิ่งเหล่านี้จะสร้างเหรียญ แต่ถ้ากระโดดเหยียบลงบนมันฝรั่งจะสร้างเหรียญได้มากกว่าเดิม นอกจากนี้ยังมีการโยนพรมประเภทต่างๆ ที่ช่วยสร้างเหรียญและเพิ่มเกจสกิลเล็กน้อย",
    "101300": "คืนชีพหลังจากพลังงานหมดลง โดยจะคืนชีพได้สูงสุด {V2} ครั้ง ครั้งละ {V1} HP ช่วยให้วิ่งต่อเนื่องไปได้ไกลขึ้นและแก้วิกฤตได้ดี",
    "103700": "เมื่อเก็บเยลลี่คำเชิญครบ 18 ชิ้น จะเริ่มปาร์ตี้พลุเหรียญ ยิงลูกกวาดดาวทำลายสิ่งกีดขวางและสร้างคะแนน ยิ่งเลเวลสูงยิ่งทำลายได้มาก และวิ่งเร็วขึ้นเมื่อเก็บไอเทมเร่งสปีด",
    "103600": "เกจสีเขียวจะเพิ่มขึ้นตามเวลา เมื่อเกจเต็มจะสร้างฟองเยลลี่ตัวอักษร Apple Cookie จะเข้าสู่โหมดโบนัสไทม์พิเศษที่มีเยลลี่ลูกโป่งปรากฏขึ้น ในตอนแรกจะวิ่งเร็วแต่จะช้าลงเมื่อ HP ลดลง",
    "100500": "เรียกปาร์ตี้พลุเหรียญออกมาเป็นระยะ ช่วยเปลี่ยนสิ่งกีดขวางเป็นเหรียญจำนวนมาก เหมาะสำหรับการฟาร์มเงิน",
    "100200": "เพิ่มเวลาในช่วง Bonus Time ให้ยาวนานขึ้น {V1} วินาที ช่วยให้เก็บคะแนนและเหรียญในด่านโบนัสได้มากขึ้น"
};

const enhancedCookies = cookiesRich.map(c => ({
    ...c,
    skill_description_en: finalizedSkills[c.id] || "Unique skill",
    skill_description_th: THAI_MECHANICS[c.id] || c.description_th || finalizedSkills[c.id] || "ความสามารถพิเศษ"
}));

const enhancedPets = petsRich.map(p => ({
    ...p,
    skill_description_en: finalizedSkills[p.id] || "Pet ability",
    skill_description_th: p.description_th || finalizedSkills[p.id] || "ความสามารถสัตว์เลี้ยง"
}));

fs.writeFileSync(path.join(__dirname, 'cookies_rich.json'), JSON.stringify(enhancedCookies, null, 2));
fs.writeFileSync(path.join(__dirname, 'pets_rich.json'), JSON.stringify(enhancedPets, null, 2));
console.log('Technical Enrichment V3 Complete');
