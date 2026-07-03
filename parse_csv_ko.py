import csv

path = "/Users/peach/Documents/cookierun file/extracted/localization_csv/l10n-ko.csv"
target_id = "1521400"

# Also try searching in the raw file if headers are missing
with open(path, mode='r', encoding='utf-8') as f:
    for line in f:
        if target_id in line:
            print(line.strip())

path2 = "/Users/peach/Documents/cookierun file/extracted/localization_csv/TreasureGrade_ko.csv"
print(f"--- Searching in {path2} ---")
with open(path2, mode='r', encoding='utf-8') as f:
    for line in f:
        if target_id in line:
            print(line.strip())
