import csv
import os
import pdfplumber

def first_number(text):
    pieces = text.replace("$", " ").split()
    number = pieces[0]
    if number == "-":
        return 0
    if "," not in number:
        number = number + pieces[1]
    return int(number.replace(",", ""))


def get_value(lines, label):
    for line in lines:
        if line.startswith(label):
            rest = line.replace(label, "")
            return first_number(rest)
    return None
    
rows = []

for filename in sorted(os.listdir("data/raw")):
    if not filename.endswith(".pdf"):
        continue

    month = filename.replace(".pdf", "")
    print("Reading", month)

    with pdfplumber.open(f"data/raw/{filename}") as pdf:
        text = pdf.pages[1].extract_text() or ""
        lines = text.split("\n")

    slots = get_value(lines, "Slot Machine Win")
    tables = get_value(lines, "Table Game Win")
    casino = get_value(lines, "Casino Win")
    internet = get_value(lines, "Internet Gaming Win")
    sports = get_value(lines, "Sports Wagering Revenue")

    if slots is None or tables is None or casino is None:
        check = "MISSING"
    elif slots < 0 or tables < 0 or casino < 0:
        check = "NEGATIVE"
    elif slots + tables == casino:
        check = "OK"
    else:
        check = "FAILED"

    rows.append([month, slots, tables, casino, internet, sports, check])

with open("data/clean/gaming_revenue.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["month", "slots", "tables", "casino_win", "internet_win", "sports_win", "check"])
    writer.writerows(rows)

print("Wrote", len(rows), "months to data/clean/gaming_revenue.csv")

print("Months that need a look:")
for row in rows:
    if row[6] != "OK":
        print(row)