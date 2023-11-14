from random import randint
from typing import List

__author__ = 'Aaron Blumenfeld'

# f(x) computes ax^2 + b for randomly chosen a, b
# findFactor finds a nontrivial factor using Pollard's Rho algorithm

# We fix an x and compute iterates f^i(x). We are looking for f^i(x) = f^j(x)
# (mod p) for p dividing n. This will mean p | f^i(x) - f^j(x), so
# gcd(f^i(x) - f^j(x), n) will give us a nontrivial factor of n (unless we're unlucky
# and every factor of n divides f^i(x) - f^j(x). We must have a collision by the
# Pigeonhole Principle (if the gcd is n, we choose a new function f -- the expectation
# for number of iterations required is sqrt(pi*p/2) <= sqrt(pi*n/4) since p <= n/2). In fact,
# one can show it's possible to find a match where j = 2i. This means we need not store
# any large tables.


def gcd(a, b):
    while b > 0:
        temp = b
        b = a % b
        a = temp
    return a


def f(x, a, b):
    return a*x*x + b


def isPrime(N):
    if N == 0 or N == 1:
        return False
    if N == 2:
        return True
    if N % 2 == 0:
        return False
    s = N-1
    while s % 2 == 0:  # write N-1 = 2^k*s
        s //= 2
    for i in range(50):  # 50 iterations has failure rate of <= 1/2^100
        a = randint(1, N-1)
        exp = s
        mod = pow(a, exp, N)
        while exp != N-1 and mod != 1 and mod != N-1:
            mod = mod * mod % N
            exp *= 2
        if mod != N-1 and exp % 2 == 0:
            return False
    return True


def findFactor(n):
    maxiterssq = 0.7854*n  # pi/4 * n
    x = randint(1, n-1)
    y = x
    d = 1
    iters = 0
    a = randint(1, n-1)
    b = randint(1, n-1)
    # a match should be found within sqrt(pi*n/2) iterations on average
    while d == 1 or d == n:
        # otherwise, choose a new function f (we may be running into a k-cycle if d == n)
        if iters*iters > maxiterssq:
            a = randint(1, n-1)
            b = randint(1, n-1)
            x = randint(1, n-1)
            y = x
            iters = 0
        x = f(x, a, b) % n
        y = f(f(y, a, b), a, b) % n
        d = gcd(abs(x-y), n)
        iters += 1
    return d


def findPrimeFactor(n, factors):
    if isPrime(n):
        factors.append(n)
    else:
        temp = n // findFactor(n)
        findPrimeFactor(temp, factors)


def factor(n, factors):
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    while n % 3 == 0:
        factors.append(3)
        n //= 3
    while n > 1:
        findPrimeFactor(n, factors)
        n //= factors[-1]


def findAllFactors(primeFactors, allFactors):
    if len(primeFactors) == 0:
        allFactors.append(1)
    elif len(allFactors) == 0:
        allFactors.append(1)
        allFactors.append(primeFactors[0])
    for i in range(1, len(primeFactors)):
        temp = []
        for f in allFactors:
            if f * primeFactors[i] not in allFactors:
                temp.append(f * primeFactors[i])
        allFactors += temp
    allFactors.sort()


def rho(n: int) -> List[int]:
    # s = ""
    # for c in 'I love cookies.':
    #    s += str(ord(c))
    # n = int(s)
    # n = 379695298917877704244229750049305390
    # n = 97201996522976692286522816012622179840
    # n = 5971474518048681630537697198080
    print("Let's factor " + str(n) + ".")
    factors = []
    factor(n, factors)
    factors.sort()
    # print("The factors are: " + str(factors) + ".")

    temp = 1
    for f in factors:
        temp *= f

    # assert (str(n-temp) == 0)

    # print("Let's multiply the factors together to make sure our result is correct. The product over our list is: " + str(temp) + ".")
    # print("...and the original number minus this product is " + str(n-temp) + ".\n")

    # print("Now let's generate a list of all factors of " + str(n) + ".")

    allFactors = []
    findAllFactors(factors, allFactors)
    # print("There are " + str(len(allFactors)) + " factors, and they are:")
    # print(allFactors)
    return allFactors


# main()
