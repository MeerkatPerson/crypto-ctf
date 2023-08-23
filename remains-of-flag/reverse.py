from Crypto.Util.number import long_to_bytes

# This challenge is really simple, only have to solve CRT. Therefore, no write-up required.

from crt import crtv1

from typing import List

# read file
file_in = open("output", "r")

# organize file lines into a list
lines = file_in.readlines()

# set up two empty lists which will be filled according to modular equations given in file
moduli: List[int] = []
primes: List[int] = []

# read modulus and prime for each equation from lines
for line in lines:

    x = line.split(",")
    moduli.append(int(x[0]))
    primes.append(int(x[1]))

# compute CRT
flag_as_long = crtv1(moduli, primes)

# flag_bytes = long_to_bytes(218774971849333696308820221317064736426417871838244359769323512140054523583409300160853956528926333)

# convert result of CRT to bytes
flag_bytes = long_to_bytes(flag_as_long)

# decode into string to reveal flag.
print(flag_bytes.decode("utf-8"))
