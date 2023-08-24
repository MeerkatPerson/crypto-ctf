from Crypto.PublicKey import RSA

from Crypto.Util.number import GCD, getPrime, inverse

import gmpy2

f = open('pubkey.pem', 'r')

key = RSA.import_key(f.read())

e = key.e

n = key.n

while True:

    x = getPrime(20)

    print("Trying " + str(x))

    x_e = pow(x, e, n)

    x_ed = 1

    for i in range(1 << 20):

        x_ed = (x_ed * x_e) % n

        g = GCD(x_ed - x, n)

        if g != 1:

            p = g
            q = n // p
            print("Solved! : " + str(p) + ", " + str(q))
