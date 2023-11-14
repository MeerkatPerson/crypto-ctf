#!/usr/bin/env python3
from Crypto.Util import number
import random
import math

from secret import flag

p = number.getPrime(1024)
q = p + (random.randint(1 << 500, 1 << 517) << 1)
while not number.isPrime(q):
    q += 2

print(f"p: {p}, q: {q}")
n = p * q
phi = (p-1) * (q-1)
e = 65537
assert math.gcd(e, phi) == 1

cipher = pow(number.bytes_to_long(flag.encode()), e, n)
print(cipher)
