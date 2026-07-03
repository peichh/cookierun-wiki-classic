import * as fs from 'fs';
import * as path from 'path';

const BASE_PATH = "/Users/peach/Documents/Poke/project/cookierun_readable_db/";
const ORIGINAL_PATH = path.join(BASE_PATH, "database/original/");
const LOC_PATH = "/Users/peach/Documents/cookierun file/extracted/localization_csv/";

function readCSV(filePath: string): any[] {
    if (!fs.existsSync(filePath)) return [];
    const content = fs.readFileSync(filePath, 'utf-8').replace(/^\uFEFF/, '');
    const lines = content.split('\n').filter(l => l.trim());
    if (lines.length === 0) return [];
    
    // Improved CSV splitter to handle quotes
    const splitCSVLine = (line: string) => {
        const result = [];
        let cur = '';
        let inQuote = false;
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            if (char === '"') inQuote = !inQuote;
            else if (char === ',' && !inQuote) {
                result.push(cur.trim());
                cur = '';
            } else cur += char;
        }
        result.push(cur.trim());
        return result;
    };

    const headers = splitCSVLine(lines[0]);
    return lines.slice(1).map(line => {
        const values = splitCSVLine(line);
        const obj: any = {};
        headers.forEach((h, i) => { 
            let val = values[i] || '';
            obj[h] = val;
        });
        return obj;
    });
}

// Load Localization for conditions
const conditionLoc = readCSV(path.join(LOC_PATH, "UnlockConditionList_ko.csv")).reduce((acc, row) => {
    acc[row._key] = row.Description_1;
    return acc;
}, {} as Record<string, string>);

// Equipment Data to map Cookie/Pet to UnlockId
const equipData = readCSV(path.join(ORIGINAL_PATH, "EquipmentDataCookieRun.csv"));
const idToUnlockId = equipData.reduce((acc, row) => {
    if (row.UnlockId && row.UnlockId !== '0') {
        acc[row._key] = row.UnlockId;
    }
    return acc;
}, {} as Record<string, string>);

// COOKIES OVERHAUL
const cookieMdPath = path.join(BASE_PATH, "characters/cookies.md");
if (fs.existsSync(cookieMdPath)) {
    const lines = fs.readFileSync(cookieMdPath, 'utf-8').split('\n');
    const newLines = lines.map(line => {
        if (!line.includes('|') || line.includes('ID | Name')) return line;
        const parts = line.split('|');
        if (parts.length < 5) return line;
        const id = parts[1].trim();
        // Match base ID (e.g. 100200 from 100201)
        const baseId = id.length === 6 ? id.slice(0, 4) + '01' : id;
        const unlockId = idToUnlockId[id] || idToUnlockId[baseId];
        const condition = (unlockId && conditionLoc[unlockId]) ? conditionLoc[unlockId] : "None (Starter/Special)";
        parts[4] = ` ${condition} `;
        return parts.join('|');
    });
    fs.writeFileSync(cookieMdPath, newLines.join('\n'));
}

// PETS OVERHAUL
const petMdPath = path.join(BASE_PATH, "characters/pets.md");
if (fs.existsSync(petMdPath)) {
    const lines = fs.readFileSync(petMdPath, 'utf-8').split('\n');
    const newLines = lines.map(line => {
        if (!line.includes('|') || line.includes('ID | Name')) return line;
        const parts = line.split('|');
        if (parts.length < 5) return line;
        const id = parts[1].trim();
        const baseId = id.length === 6 ? id.slice(0, 4) + '01' : id;
        const unlockId = idToUnlockId[id] || idToUnlockId[baseId];
        const condition = (unlockId && conditionLoc[unlockId]) ? conditionLoc[unlockId] : "None (Starter/Gacha)";
        parts[4] = ` ${condition} `;
        return parts.join('|');
    });
    fs.writeFileSync(petMdPath, newLines.join('\n'));
}

console.log("Unlock conditions updated successfully.");
