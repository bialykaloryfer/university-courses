import timeit

def imperative_primes(n):
    res = [True] * n
    res[0] = res[1] = False

    i = 2
    while i * i <= n:
        if res[i]:
            for j in range(i * i, n, i):
                res[j] = False                   
        i += 1
 
    primes = []
    for i in range(n):
        if res[i]:
            primes.append(i)

    return primes

def compose_primes(n):
    primes = [True if all(i % j != 0 for j in range(2, int(i**0.5) + 1)) else False for i in range(2, n)]
    return [i for i in range(2, n) if primes[i - 2] == True]

def functional_primes(n):

    def is_prime(x):
        if x < 2:
            return False
        for i in range(2, x):
            if x % i == 0: 
                return False
        return True

    return list(filter(is_prime, range(n)))


print("n    imper.  sklad.  funk.")

for n in range(10, 100, 10):
    s = round(timeit.timeit(lambda: imperative_primes(n), number=n), 4)
    i = round(timeit.timeit(lambda: compose_primes(n), number=n), 4)
    f = round(timeit.timeit(lambda: functional_primes(n), number=n), 4)
    print(str(n) + ": " + " {:.4f}  ".format(s) + "{:.4f}  ".format(i) + "{:.4f}".format(f))
