
# Firstly, we need to break RSA using the given parameters.

# Then, we need to reverse the Optimal asymmetric encryption padding performed in chall.py (https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding).

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

from hashlib import sha256
import random

from crt import crtv1
from decimal import *

import sys

import gmpy2

sys.setrecursionlimit(1500)

# Since we have 3 ciphertexts that were encrypted with different public keys using e = 3 each time, we can compute the Chinese Remainder thm. using the three n's from the three different public keys (public keys = [(n=n1,e=3),(n=n2,e=3),(n=n3,e=3)]) and the three ciphers to compute a solution to the CRT:
# (I) x = c1 mod n1
# (II) x = c2 mod n2
# (III) x = c3 mod n3
# .... then, the 3rd root of x is our decrypted message.
# source: https://crypto.stackexchange.com/questions/52504/deciphering-the-rsa-encrypted-message-from-three-different-public-keys

n1 = 25926008196418567463152673374042317701109256935740230056241016011301506719623259681126159071612387692584060159863136690864062544204035602029089483431920875340423957871836839972708100406737369348138063433839236934931157873662506538922790236371279799070064035778137972485178248255920685317034730364966724803058971802219237207375135423310613229247389383238143547318241162872479294472257380218319496323519380446745787159573184245110326773051189202066215822548047958974625334022850881443332592769064541253014817576285787829984248841745087152813303365653896524105315805959820952113094357693874057656949443725424170404582137

c1 = int("0x2ad2290a081acee41b123a8a8aeb890c2289b96dd23076c2a6b2a75767c3f4ea325be45f2381d2a42f7223da93fb4248e8636393030bf8ef332108dfa820338980ab549bb05ecc3b3aaa1a8befd643e3cc0bb5dbb7f116598b6d16c4f93a9a9bdd07c96df0fad4df9eb66f0a8e10ee5cef2286fe7eec239e847ace7009ca6842fe2cf90796c772755e0ec90a69c5363eae278059dc1f8b8140a06be3f2c46d45850768066d185f507f2eed2b4679816207e499633e5a88ea1a35117e6ffa82629b37e4cac3fa3a6f57d97b8108372ec090ef4505f0db8d467e656f0289ee27a448f973aac49fb1004c7e2d0d5f870950ebe9042d16282d27d38a8a1fb03f5418", 16)

n2 = 29270259642244474300734282705455424650211470710445285571537066939805411760818254058414722115336311695965214643322869642239133397668500184296711197442350652831732871773121239484791204857797042900138680641186028776887223063436396771140227801369179759856224314219464967549241784575945593253754083082131727185043092493251247778555481095596792942538909262492411418300581018581904935590415562470430568698556363456918216110915931647101003482031496007462067201248736242534178963465333219891069009819597949899883716685661145012089576340613712033554611406512071752222174062495117199335410083246608320105042312201219930039249721

c2 = int("0x6a9172cb9a2f09d8e52114b35c038dbe34ef6332acee4a567de6bb0ede63954d18f96baba0a1d24409cd464b05176611bdd275ef1f00d65ee80ca66ef5002b8b57a86429fe86f5cf5e1152f7217bdf1c64d8a598a9f1df90f9ac1af172a92a33ce621d78abc36f18da54d9c8b528616211f55f114295c4bcddea89256d721acbd9ed2a8a8966b8c37d21b924e6542362c7e706f867b11dac2316381d9c2621b7df3916714f0b9e7333a4cffcfd685c4512d93ad3a59b2a9506f27944d36229d51a63e39336ccf3e1a3555ba380b87f5308d1580a4b99b85ad458624ea4ca856bea199302b9a3c2cbd416292f33d7041e5cb7488acc0114ff580f68fc66293ebd", 16)

n3 = 19216298446687659731722104164559043900218697807039369442598601680047859135202892202828176900034599970785456479580726329592001366288946428954093064050700787908069349721929190887179909127852148688458967322556129049724955415267317704200379978719535566975656069119466718488186780211196506151219634855230164845126166224410878285685863468026684895453026437342995422186599664391786951425625781245215549479031943820343505112791833308745219365168498356627984039479424491639128060856763969144012054230601519131143419102191169538234121458250065787286741854146963420206139674321213607232550562417520299605556452707285825597189193

c3 = int("0x3fee4c6938f2cc81d4c975cbc856de692735a42fac60ae0c5728e760dd1fef30ec50d00c6b30d9c38abf7495f37fce2392e7cf72d30c09dbbe7c70d1c49afb14cdacb41a9a5160160ad4add033d048f2fd550dc589248e4f2630cd2b2a3e2dfec6783288bd2f9a5fb1c3310257ecff428216158a4221fb616f011f5ff11134fe0db56664da4bb3d74a933217dc8c447f653b23d4aa5c0c024629834a1a9d259ac372e71666dc6efe932da3aaa8e9ebfe199d9f9faeb71d92f284ede69a818f86121434f83611c5c6c0c3d099595f77015f07325420fbe6c2e4a481a229c0cbbef88cb21943e71661900067a4de36f4f68cd68b0ed444dd85e76e0a731e8e185c", 16)

# Parameters
N = 2048   # key length in bits
hLen = 256 # hash length in bits

# Pt. 1: decrypt

# compute CRT
c = crtv1([c1, c2, c3], [n1, n2, n3])

# print(f'c: {c}')

# sanity check: ensure solution is correct
assert(c1 == (c % n1))
assert(c2 == (c % n2))
assert(c3 == (c % n3))

# use cool function for modular root, avoiding overflow
m = gmpy2.iroot(c, 3)

# sanity check: ensure encoding m with the three keys gives the three ciphers
assert(c1 == ((int(m[0]) ** 3) % n1))
assert(c2 == ((int(m[0]) ** 3) % n2))
assert(c3 == ((int(m[0]) ** 3) % n3))

# ****************************************************************

# Pt. 2: Now, we need to reverse the padding.

# label hash
lHash = sha256(b'').digest()

# convert our decrypted cipher to a 256 byte ( = 2048//8) byte array
EM = long_to_bytes(int(m[0]), 256)

# decompose the byte array into its components
# know that we first have one 0 byte (1 byte), then maskedSeed of length 256 // 8 = 32 bytes, and thereafter maskedDB of length = 256 - 32 - 1 = 223
_, maskedSeed, maskedDB = EM[:1], EM[1:1 + 32], EM[1 + 32:]
# maskedSeed and maskedDB are of type <class 'bytes'>

# need our custom MGF function from chall.py now:
def MGF(seed, length):
    random.seed(seed)
    return [random.randint(0,255) for _ in range(length)]

# compute seed mask using maskedDB and length of hash in bytes (32 for sha256)
# can directly call 'bytes_to_long' on maskedDB since it is already of type <class 'bytes'>
seedMask = MGF(bytes_to_long(maskedDB), 32)

# recover seed by XOR-ing masked seed with seedmask
seed = [maskedSeed[i] ^ seedMask[i] for i in range(32)]

# generate DBMask:
# here we need to cast seed to a <class 'bytes'> object first before we can call 'bytes_to_long' as it is currently a list/byte-array
dbMask = MGF(bytes(seed), 256 - 32 - 1)

# recover DB:
DB = [maskedDB[i] ^ dbMask[i] for i in range(256 - 32 - 1)]

# now split DB into its parts: lHash'||PS||0x01||M 
_lHash = DB[:32]

print(f'lHash: {lHash}, _lHash: {bytes(_lHash)}')

if not lHash == bytes(_lHash):
    print("lHash' not equal to lHash")

i = 32

# now we want to walk through the remainder of DB until we encounter a 1.
while i < len(DB):
    if DB[i] == 0:
        i += 1
        continue
    elif DB[i] == 1:
        i += 1
        break
    else:
        raise Exception("invalid padding")
M = DB[i:]

print(bytes(M).decode())