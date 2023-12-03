#tekst ze strony
#https://www.gutenberg.org/cache/epub/1513/pg1513.txt

from random import randint

def simplify(text, dl, ls):
    text = text.split()
    new = []

    for i in range(len(text)):
        if len(text[i]) > dl:
            continue
        else:
            new.append(text[i])

    for i in range(len(new) - ls):
        new.pop(randint(0, len(new) - 1))

    return new

tekst = "Podział peryklinalny inicjałów wrzecionowatych kambium charakteryzuje się ścianą podziałową inicjowaną w płaszczyźnie maksymalnej."
result = simplify(tekst, 10, 5)
print(result)

with open("Romeo.xml", "r", encoding='utf-8') as f:
    f = f.read()
    result = simplify(f, 10, 50)
    print(result)