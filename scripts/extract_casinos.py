import pdfplumber

def all_numbers(text):
    pieces = text.replace("$", " ").split()
    numbers = []
    leftover = ""
    for piece in pieces:
        if piece == "-":
            number.append(0)
            leftover = ""
        elif "," in piece:
            numbers.append(int((leftover + piece).replace(",", "")))
            leftover = ""
        elif piece.isdigit():
            leftover = piece
        elif piece.isdigit():
            leftover = ""
    return numbers

casinos = ["Bally's", "Borgata", "Caesars", "Golden Nugget", "Hard Rock", "Harrah's", "Ocean Casino", "Resorts", "Tropicana"]

filename = "data/raw/2026-09.pdf"

with pdfplumber.open(filename) as pdf:
    text = pdf.pages[3].extract_text() or ""
    lines = text.split("\n")

floor_total = 0

for line in lines:
    if line.startswith("Total"):
        break
    for casino in casinos:
        if line.startswith(casino):
            numbers = all_numbers(line)
            slots = numbers[0]
            tables = numbers[2]
            floor = numbers[4]
            print(casino, floor, slots + tables == floor)
            floor_total = floor_total + floor

print("Floor total:", floor_total)
print("Should be: ", 227797045)