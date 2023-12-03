import math
from random import uniform

def pi_approximation(appr):
    n = 1_000_000
    in_o = 0
    curr = 0

    for x in range(n):
        curr += 1
        x = uniform(-100, 100)
        y = uniform(-100, 100)
        if (math.sqrt(x ** 2 + y ** 2) <= 100):
            in_o += 1
        new_pi = 4 * in_o / curr
        print(new_pi)

        if(abs(new_pi - math.pi) < appr):
            break

print(pi_approximation(0.00001))