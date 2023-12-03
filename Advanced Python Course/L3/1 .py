def longest_palidnrom(text):
    text = "$#" + "#".join(text) + "#@"
    n = len(text)
    values = [0] * n

    mid = 0
    right = 0

    max_ = 0
    idx = 0

    for i in range(1, n - 1):
        mirr = 2 * mid - i
    
        if right - i > 0:
            values[i] = min(values[mirr], right - i)

        while text[i  + (1 + values[i])] == text[i - (1 + values[i])]:
            values[i] += 1

        if values[i] > max_:
            max_ = values[i]
            idx = i

        if i + values[i] > right:
            mid = i
            right = i + values[i]

  
    start = (idx - max_) // 2
    end = start + max_ 

    return (start, end)


print(longest_palidnrom("gggssssshahaaaadddaaaahwo"))
