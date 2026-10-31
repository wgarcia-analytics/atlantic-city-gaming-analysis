import pdfplumber

def all_numbers(text):
    text = text.replace("$", " ").replace("(", " ( ").replace(")", " ) ")
    pieces = text.split()
    numbers = []
    leftover = ""
    negative = False
    for piece in pieces:
        if piece == "(":
            negative = True
        elif piece == ")":
            negative = False
        elif piece == "-":
            numbers.append(0)
            leftover = ""
        elif "," in piece:
            number = int((leftover + piece).replace(",", ""))
            if negative:
                number = -number
            numbers.append(number)
            leftover = ""
        elif piece.isdigit():
            leftover = piece
        else:
            leftover = ""
    return numbers
    
def split_name(line):
    name_pieces = []
    for piece in line.split():
        if piece[0].isdigit() or piece[0] == "$" or piece == "-" or piece == "(":
            break
        if piece[0] == "(" and piece[1].isdigit():
            break
        name_pieces.append(piece)
    return " ".join(name_pieces)

casinos = ["Bally's", "Borgata", "Caesars", "Golden Nugget", "Hard Rock", "Harrah's", "Ocean Casino", "Resorts", "Tropicana"]

filename = "data/raw/2026-09.pdf"

with pdfplumber.open(filename) as pdf:
    text = pdf.pages[3].extract_text() or ""
    lines = text.split("\n")
    online_text = pdf.pages[4].extract_text() or ""
    online_lines = online_text.split("\n")

floor_total = 0
floor_by_casino = {}

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
            floor_by_casino[casino] = floor

print("Floor total:", floor_total)
print("Should be: ", 227797045)

online_total = 0
online_by_casino = {}
for casino in casinos:
    online_by_casino[casino] = 0

for line in online_lines:
    if line.startswith("Total"):
        break
    name = split_name(line)
    for casino in casinos:
        if name.endswith(casino) or name.endswith(f"CIENJ ({casino})"):
            amount = all_numbers(line)[0]
            online_by_casino[casino] = online_by_casino[casino] + amount
            online_total = online_total + amount
            break

print("Online total:", online_total)
print("Should be:   ", 274782098)

for casino in casinos:
    floor = floor_by_casino[casino]
    online = online_by_casino[casino]
    print(f"{casino:15} {floor:>12,} {online:>12,} {online / floor:6.2f}")