#https://www.gutenberg.org/cache/epub/1513/pg1513.txt

def compress(text):
    compressed = []
    i = 0
    count = 1

    while i < len(text) - 1:
        if text[i] == text[i + 1]:
            count += 1
            i += 1
        else:
            compressed.append((count, text[i]))
            i += 1
            count = 1
    print(i)
    compressed.append((count, text[i]))

    return compressed
    
def decompress(xs):
    txt = ""

    for x in xs:
        for i in range(x[0]):
            txt += x[1]

    return txt

with open("Romeo.xml", 'r', encoding='utf-8') as f:
    f = f.read()
    com = compress(f)
    print(decompress(com))