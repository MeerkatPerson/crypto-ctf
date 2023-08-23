from typing import List

import socket

k: int = 6

two_pow_k: int = 2**k


def brauer_k(n: int) -> List[int]:

    if n < two_pow_k:

        return [i for i in range(1, two_pow_k)]

    else:

        q: int = n // two_pow_k

        q_chain: List[int] = brauer_k(q)

        two_pow_chain: List[int] = [q*pow(2, i) for i in range(1, k+1)]

        return q_chain + two_pow_chain + [n]


def process_chain(chain: List[int]):

    max: int = chain[0]

    new_chain = [1]

    for i in range(1, len(chain)):

        if (chain[i] > max):
            new_chain.append(chain[i])
            max = chain[i]

    return new_chain


def get_add(chain: List[int]):

    addends: List[int] = [1]

    for i in range(1, len(chain)):

        addends.append(chain[i] - chain[i-1])

    return addends


n: int = 1541111950826012932818579917878115126891515189026461632309297706194099868429854707691081039238166336538765649605121690421278157704079519667964225882373835268572210132969514200652515806070417542358288870470825376486211803610904321939871571621034754297583265143917317205436069844507707418920641432285502834503074152732414055128592923014277151376748376274385713023781739768580201137449799263309469494028862323073902193471157524645576410306515325631842834325277276854799886178480595612297844929470119630717050537040693061171289159913780666851216952647663392292235756345159690805601196136527674544011018988336791940912417

n_chain: List[int] = brauer_k(n)

processed_chain: List[int] = process_chain(n_chain)

add_chain: List[int] = get_add(processed_chain)

print(f'Length of add chain: {len(add_chain)}')

print(add_chain[:128])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("servicevm.enoflag.de", 10002))

for i in range(1, len(add_chain)):

    chunk = s.recv(4000)

    print(chunk)

    if b"I haven't" in chunk:
        break

    print("sending %d" % add_chain[i])

    number = str(int(add_chain[i])) + '\n'

    s.send(number.encode())

chunk = s.recv(4000)

print(chunk)

print("sending 0")
number = str(0) + '\n'

s.send(number.encode())

while True:

    chunk = s.recv(4000)

    print(chunk)
