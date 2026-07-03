import csv

path = "/Users/peach/Documents/cookierun file/extracted/localization_csv/StuffName_ko.csv"
target_id = "1521400"

with open(path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['_key'] == target_id:
            print(f"Name: {row['Name']}")
            print(f"DetailDescription: {row['DetailDescription']}")
            print(f"SubDescription: {row['SubDescription']}")
            break
