import * as fs from 'fs';

const STUFF_NAME_PATH = "/Users/peach/Documents/cookierun file/extracted/localization_csv/StuffName_ko.csv";
const TREASURE_GRADE_PATH = "/Users/peach/Documents/cookierun file/extracted/localization_csv/TreasureGrade.csv";

function findLine(filePath: string, target: string) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');
    return lines.filter(line => line.includes(target));
}

console.log("--- Resolving Treasure ID 569 ---");

const gradeLines = findLine(TREASURE_GRADE_PATH, ",569");
console.log("Lines in TreasureGrade.csv:", gradeLines);

// Extract the primary key (often the first or second column)
// From previous grep: 1,12,0,0,S,1521400,569
// Let's look for 1521400 in StuffName_ko.csv

const stuffLines = findLine(STUFF_NAME_PATH, "1521400");
console.log("Lines in StuffName_ko.csv for 1521400:", stuffLines);

// Also search for "569" directly in StuffName_ko.csv again
const directStuffLines = findLine(STUFF_NAME_PATH, ",569");
console.log("Direct search for ,569 in StuffName_ko.csv:", directStuffLines);
