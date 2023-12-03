import re

def format_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ''.join(text.split())
    return text

def is_palindrom(text):
    text = format_text(text)   
    i = 0
    j = len(text) - 1

    while i != j:
        if text[i] != text[j]:
            return False
        else:
            i += 1
            j -= 1
    return True

print(is_palindrom("Eine güldne, gute Tugend: Lüge nie!"))
print(is_palindrom("Míč omočím."))
print(is_palindrom(",k a ; j a   :k "))
print(is_palindrom("to nie jest palindrom"))