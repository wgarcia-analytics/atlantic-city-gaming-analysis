import pdfplumber

def first_number(text):
    pieces = text.replace("$", " ").split()
    number = pieces[0]
    if "," not in number:
        number = number + pieces[1]
    return int(number.replace(",", ""))


def get_value(lines, label):
    for line in lines:
        if line.startswith(label):
            rest = line.replace(label, "")
            return first_number(rest)
    return None
    
filename = "data/raw/2017-01.pdf"

with pdfplumber.open(filename) as pdf:
    text = pdf.pages[1]. extract_text() or ""
    lines = text.split("\n")

slots = get_value(lines, "Slot Machine Win")
tables = get_value(lines, "Table Game Win")
casino = get_value(lines, "Casino Win")
internet = get_value(lines, "Internet Gaming Win")
sports = get_value(lines, "Sports Wagering Revenue")

print("Slots:", slots)
print("Tables:", tables)
print("Casino Win:", casino)
print("Internet Gaming Win:", internet)
print("Sports Wagering:", sports)

if slots + tables == casino:
    print("Check passed: slots + tables = casino win")
else:
    print("CHECK FAILED: slots + tables does not equal casino win")
