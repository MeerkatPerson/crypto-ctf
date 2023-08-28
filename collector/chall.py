from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha256
import random

# from secret import flag

# Parameters
N = 2048
hLen = 256


def MGF(seed, length):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]


def pad(stream, bitlength, tag=b''):
    seed = sha256(stream).digest()
    DB = sha256(tag).digest() + b'\x00' * ((bitlength - 16 -
                                            2*hLen) // 8 - len(stream)) + b'\x01' + stream
    print(f'len(DB): {len(DB)}')  # 223
    mask = MGF(seed, len(DB))
    maskedDB = [DB[i] ^ mask[i] for i in range(len(DB))]
    seedmask = MGF(bytes_to_long(bytes(maskedDB)), hLen // 8)
    masked_seed = [seed[i] ^ seedmask[i] for i in range(hLen // 8)]
    EM = [0] + masked_seed + maskedDB
    return bytes(EM)


for i in range(0, 4):

    print((1 << (1 << i)) + 1)

key = RSA.generate(N, e=(1 << (1 << random.randint(0, 4))) + 1)
flag = "it'S_lit".encode()
msg = pad(flag, N)
cipher = pow(bytes_to_long(msg), key.e, key.n)
print(key.publickey().export_key())
print(key.d)
print(hex(cipher))
