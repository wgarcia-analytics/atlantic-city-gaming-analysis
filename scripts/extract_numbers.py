def first_number(text):
    pieces = text.replace("$", " ").split()
    number = pieces[0]
    if "," not in number:
        number = number + pieces[1]
    return int(number.replace(",", ""))


print(first_number("294,904,367 311,912,857 (17,008,490) (5.5)"))
print(first_number("7 2,545,070 7 7,583,668 ( 5,038,598) (6.5)"))
print(first_number("$ 1 23,662,620 $ 122,906,035 $ 756,585 0.6"))
print(first_number("2 ,129,453,651 1 ,881,623,639"))