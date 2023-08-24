#!/usr/bin/env sage

from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
import time
import sys
# from secret import flag

key = RSA.import_key(open('pubkey.pem', 'r').read())


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


def encrypt(msg, key=key):
    return pow(str_to_int(msg), key.e, key.n)


def decrypt(cipher, key=key):
    return int_to_str(pow(cipher, key.d, key.n))


def decrypt_fast(cipher, key=key):
    d_p = key.d % (key.p - 1)
    d_q = key.d % (key.q - 1)
    m_p = pow(cipher % key.p, d_p, key.p)
    m_q = pow(cipher % key.q, d_q, key.q)
    h = key.u * (m_p - m_q) % key.p
    m = m_q + h*key.q % key.n
    return int_to_str(m)


def loop():
    enc_flag = encrypt(f)
    print('Ain\'t nobody got time for slow algos ...\nWanna see how much difference a clever decryption makes, e.g. for this encrypted flag:\n%s\nBut you can also enter some other cipher in hex: ' %
          hex(enc_flag)[2:])
    while True:
        sys.stdout.flush()
        cipher = sys.stdin.buffer.readline().strip()
        if len(cipher) > 512:
            print('Input too long')
            continue
        try:
            c = int(cipher, 16)
        except:
            print('Wrong input format')
            continue

        t0 = time.time()
        m = decrypt(c)
        print('plain decryption: %.2f ms' % ((time.time() - t0) * 1000))
        t0 = time.time()
        m = decrypt_fast(c)
        print('fast decryption: %.2f ms' % ((time.time() - t0) * 1000))
        print('another cipher: ')


if __name__ == '__main__':
    print(len("flag{e4ch_m0dulus_g1ves_s0m3_inf0rmat1on}"))
    print(len("flag{do3s_an_4ddition_cha1n_have_a_w3ake5t_link}"))
    print(len("flag{com3_to_my_p4rty_bu1_do_n0t_tel1_B0b}"))
    enc_flag = encrypt("f00000000000000000000000000000000")
    print(hex(enc_flag))
    enc_flag = encrypt("faaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print(hex(enc_flag))
    """
    try:
        loop()
    except Exception as err:
        print(repr(err))    
    """
