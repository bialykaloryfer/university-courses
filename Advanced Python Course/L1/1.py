from decimal import Decimal

def vat_faktura(lst):
    s = 0
    for i in lst:
        s += i
    return s * 0.23

def vat_paragon(lst):
    s = 0
    for i in lst:
        s += (0.23 * i)
    return s

def vat_faktura_dec(lst):
    s = Decimal(0)
    for i in lst:
        s += i
    return s * Decimal(0.23)

def vat_paragon_dec(lst):
    s = Decimal(0)
    for i in lst:
        s += (Decimal(0.23) * i)
    return s

zakupy = [0.12, 2.79, 3.09, 4.57]
zakupy_dec = [Decimal(0.12), Decimal(2.79), Decimal(3.09), Decimal(4.57)]

print(vat_faktura(zakupy) == vat_paragon(zakupy))
print(vat_faktura_dec(zakupy_dec) == vat_paragon_dec(zakupy_dec))
