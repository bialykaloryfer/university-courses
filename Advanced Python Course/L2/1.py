
def dhondt(wyn, man):
    s = sum(i[0] for i in wyn)  
    res = []
    wyn = [i for i in wyn if i[0] > s * 0.05]

    for i in range(len(wyn)):
        for j in range(1, man + 1):
            res.append((wyn[i][0] // j, wyn[i][1]))

    res.sort(key=lambda x: x[0], reverse=True)
    allocated_seats = {}

    for i in range(man):
        party = res[i][1]
        if party not in allocated_seats:
            allocated_seats[party] = 0
        allocated_seats[party] += 1

    return allocated_seats

print(dhondt([(720, "A"), (500, "B"), (900, "C")], 10))