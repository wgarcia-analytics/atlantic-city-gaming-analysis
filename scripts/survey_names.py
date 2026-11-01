import os
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
        elif "," in piece and (leftover + piece).replace(",", "").isdigit():
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

count = {}
first_seen = {}
last_seen = {}

for filename in sorted(os.listdir("data/raw")):
    if not filename.endswith(".pdf"):
        continue
    month = filename.replace(".pdf", "")
    if month >= "2025-01":
        continue

    with pdfplumber.open(f"data/raw/{filename}") as pdf:
        text = pdf.pages[2].extract_text() or ""

    for line in text.split("\n"):
        name = split_name(line)
        if name == "" or len(all_numbers(line)) == 0:
            continue
        if name not in count:
            count[name] = 0
            first_seen[name] = month
        count[name] = count[name] + 1
        last_seen[name] = month

for name in sorted(count):
    print(f"{name:35} {count[name]:3}   {first_seen[name]} to {last_seen[name]}")