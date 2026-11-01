import os
import csv
import pdfplumber
import pandas as pd
from helpers import all_numbers, split_name, clean_name

units = ["Bally's", "Borgata", "Caesars", "Caesars Interactive NJ", "Golden Nugget",
         "Hard Rock", "Harrah's", "Ocean Casino", "Resorts", "Tropicana"]

name_map = {
    "Bally's AC": "Bally's",
    "Bally's (CEI)": "Bally's",
    "Bally's (Premier)": "Bally's",
    "Bally's": "Bally's",
    "Borgata": "Borgata",
    "Caesars": "Caesars",
    "Caesars Interactive NJ": "Caesars Interactive NJ",
    "Golden Nugget": "Golden Nugget",
    "GNOG": "Golden Nugget",
    "Hard Rock": "Hard Rock",
    "Harrah's": "Harrah's",
    "Ocean Resort": "Ocean Casino",
    "Ocean Casino": "Ocean Casino",
    "Resorts": "Resorts",
    "Resorts Digital": "Resorts",
    "Tropicana": "Tropicana",
}

def read_old(pdf):
    floor = {}
    online = {}
    for unit in units:
        floor[unit] = 0
        online[unit] = 0

    text = pdf.pages[2].extract_text() or ""
    for line in text.split("\n"):
        name = clean_name(split_name(line))
        if name in name_map:
            unit = name_map[name]
            numbers = all_numbers(line)
            floor[unit] = floor[unit] + numbers[0]
            online[unit] = online[unit] + numbers[2]

    return floor, online
    
def read_new(pdf):
    floor = {}
    online = {}
    for unit in units:
        floor[unit] = 0
        online[unit] = 0

    text = pdf.pages[3].extract_text() or ""
    for line in text.split("\n"):
        if line.startswith("Total"):
            break
        name = clean_name(split_name(line))
        if name in name_map:
            unit = name_map[name]
            floor[unit] = floor[unit] + all_numbers(line)[4]
        
    text = pdf.pages[4].extract_text() or ""
    for line in text.split("\n"):
        if line.startswith("Total"):
            break
        name = split_name(line)
        unit = None
        if "CIENJ" in name:
            unit = "Caesars Interactive NJ"
        else:
            for casino in units:
                if name.endswith(casino):
                    unit = casino
        if unit is not None:
            online[unit] = online[unit] + all_numbers(line)[0]

    return floor, online
                           
totals = pd.read_csv("data/clean/gaming_revenue.csv")

rows = []
problems = []

for filename in sorted(os.listdir("data/raw")):
    if not filename.endswith(".pdf"):
        continue
    month = filename.replace(".pdf", "")

    with pdfplumber.open(f"data/raw/{filename}") as pdf:
        if month < "2025-01":
            floor, online = read_old(pdf)
        else:
            floor, online = read_new(pdf)

    row = totals[totals["month"] == month]
    floor_gap = sum(floor.values()) - row["casino_win"].iloc[0]
    online_gap = sum(online.values()) - row["internet_win"].iloc[0]

    if floor_gap != 0 or online_gap != 0:
        problems.append([month, floor_gap, online_gap])

    for unit in units:
        rows.append([month, unit, floor[unit], online[unit]])

with open("data/clean/casino_monthly.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["month", "unit", "floor_win", "online_win"])
    writer.writerows(rows)

print("Wrote", len(rows), "rows")

for problem in problems:
    print("PROBLEM:", problem)
