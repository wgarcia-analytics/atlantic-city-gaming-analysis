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

def clean_name(name):
    for mark in [" (a)", " (b)", " (c)"]:
        name = name.replace(mark, "")
    return name
