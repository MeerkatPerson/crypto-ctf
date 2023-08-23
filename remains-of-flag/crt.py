
from typing import List, Tuple
from operator import mul
from functools import reduce

# Extended Euclidean Algorithm
# Input: two numbers a, b
# Output: gcd of the two input numbers as well as factors lambda, mu for representing gcd as a linear combination of the two input numbers, i.e., such that gcd(a,b) = lambda*a + mu*b
def EEA(a: int, b: int) -> Tuple[int, int, int]:

    if b == 0:
        return (a, 1, 0)

    d, s, t = EEA(b, a % b)

    return (d, t, s - (a//b) * t)

# nasty looking implementation of chinese remainer theorem, trying to not use loops
# see examples in main below
def crtv1(remainders: List[int], primes: List[int]) -> int:

    bs: List[int] = list(map(lambda x: reduce(
        mul, filter(lambda y: y != x, primes), 1), primes))

    eeas: List[int] = list(
        map(lambda y: EEA(y[0], y[1]), zip(bs, primes)))
    b_invs: List[int] = list(map(lambda x: x[1], eeas))

    prods: List[int] = list(map(lambda x: x[0]*x[1]*x[2],
                                zip(remainders, bs, b_invs)))

    return sum(prods) % reduce(mul, primes)


if __name__ == "__main__":

    # represent the system of modular equations:
    # x = 1 mod 3
    # x = 2 mod 5
    # x = 3 mod 7
    print(crtv1([1, 2, 3], [3, 5, 7]))

    # system of modular equations from given 'output' file
    print(crtv1([12351174652798784358, 2226709634574810886, 6693257220091591654, 10944103399392434542, 10904614792695064769, 9596120144205116755], [
          16590847301177859509, 9941423676834502901, 13870307907550356091, 11534029519943368591, 11859273536079686581, 17523447057493133641]))
