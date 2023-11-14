from Crypto.Util.number import bytes_to_long, long_to_bytes
from itertools import combinations
from operator import mul
from functools import reduce
from typing import Tuple
import socket
from Crypto.PublicKey import RSA


def int_to_str(n):
    if n == 0:
        return ''
    return int_to_str(n // 256) + chr(n % 256)


def str_to_int(s):
    res = 0
    for char in s:
        res *= 256
        res += ord(char)
    return res

# check if a divisor fulfills the servers requirements

def is_valid_divisor(div: int) -> Tuple[bool, int]:

    div_bytes = long_to_bytes(div)

    if b'cookie' in div_bytes or any([c < 32 for c in div_bytes]):

        return (False, None)

    return (True, int_to_str(div))


num = str_to_int('I love cookies.')  # 379695298917877704244229750049305390

key = RSA.importKey(open('pubkey.pem', 'r').read())

# prime factorization of 'num'
factors = [2, 5, 6673, 189344417922901, 30051184098398543]

# compute all subsets of valid_divisors
subsets = sum(map(lambda r: list(combinations(factors, r)),
                  range(1, len(factors)+1)), [])

# map the subsets to lists
subset_lists = list(map(lambda s: list(s), subsets))

# derive divisors
divisors = list(
    map(lambda x: reduce(mul, x, 1), subset_lists))

# map to tuples of the form (subset, prod), e.g. ([32, 64], 32*64)
# subset_lists_tuples = list(
#    map(lambda x: (x, reduce(mul, x, 1)), subset_lists))

valid_divisors = []

# print(divisors)

# print(subset_lists_tuples)

for divisor in divisors:

    eval, str_fact = is_valid_divisor(divisor)

    if (eval):

        print(f"Factor: {divisor}, factor as string: {str_fact}")

        valid_divisors.append(divisor)

# print(valid_divisors)

# compute all subsets of valid_divisors
subsets_valid_divisors = sum(map(lambda r: list(combinations(valid_divisors, r)),
                                 range(1, len(valid_divisors)+1)), [])

# map to lists
subset_valid_divisors_lists = list(
    map(lambda s: list(s), subsets_valid_divisors))

valid_divisor_products = list(
    map(lambda x: (x, reduce(mul, x, 1)), subset_valid_divisors_lists))

# print(valid_divisor_products)

match = None

for valid_divisor_product in valid_divisor_products:

    if valid_divisor_product[1] % key.n == num:

        # Success: [30051184098398543, 12634953007995183730]
        print(f"Success: {valid_divisor_product[0]}")

        match = valid_divisor_product[0]

        for fact in valid_divisor_product[0]:

            print(int_to_str(fact))

print(
    f"Sanity check: {30051184098398543 * 12634953007995183730}, {30051184098398543 * 12634953007995183730 == num}, {match[0] * match[1] == num}, {str_to_int('I love cookies.') == num}, {int_to_str(30051184098398543)}, {int_to_str(12634953007995183730)}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("servicevm.enoflag.de", 10008))

# receive instructions from server
chunk1 = s.recv(36000)

print(chunk1)

# send our first factor
# payload_1 = "1:" + int_to_str(30051184098398543) + "\n"
payload_1 = '1:'.encode() + long_to_bytes(match[0]) + '\n'.encode()

s.send(payload_1)

chunk2 = s.recv(36000)

print(chunk2)

sig1 = int(chunk2.decode().split('\n')[0])

print(sig1)

assert (pow(sig1, key.e, key.n) == match[0])

# payload_2 = "1:" + int_to_str(12634953007995183730) + "\n"
payload_2 = '1:'.encode() + long_to_bytes(match[1]) + '\n'.encode()

s.send(payload_2)

chunk3 = s.recv(36000)

sig2 = int(chunk3.decode().split('\n')[0])

print(sig2)

assert (pow(sig2, key.e, key.n) == match[1])

print(sig2)

# sig_full = (sig1 * sig2) % n  # resp. without the mod n??
sig_full = sig1 * sig2

assert (pow(sig_full, key.e, key.n) == num)

print(sig_full)

payload_3 = '2:' + str(sig_full) + '\n'

s.send(payload_3.encode())

chunk4 = s.recv(36000)

print(chunk4)
