from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA

bitlen = 2048

names = ['ROD EARNEST ANDREW MCINTYRE',
         'MARION SHELBY BRICE MONTOYA',
         'HAZEL YVONNE ABIGAIL PRINCE']

base = ' ' * len(names[0])

n = []

c = []

for i in range(3):

    key = RSA.generate(bitlen, e=3)

    msg = "Dear " + names[i] + " flag{c00l}"

    n.append(key.n)

    c.append(pow(bytes_to_long(msg.encode()), 3, key.n))

print(n)

print(c)
