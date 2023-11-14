from typing import List, Dict
from crt import crt_generalized
from chall import Permutation, pow
from Crypto.Cipher import AES
import ast

file = open('output', 'r')

lines = file.readlines() # the individual lines of 'output' are: p, A, B, enc_flag

# helper def for extracting int lists from str file lines
def get_as_int_list(str: input) -> List[int]:

    chunks = str.split('= ')

    myList = ast.literal_eval(chunks[1])

    myIntList = [int(x) for x in myList]

    return myIntList

p = get_as_int_list(lines[0])

A = get_as_int_list(lines[1])

B = get_as_int_list(lines[2])

assert(max(p) == len(p)-1)

# extract disjoint cycles; this should work

def getCycles(myPerm: List[int]) -> List[List[int]]:

    cycles = []

    mappings = dict()

    # for eficiency, store in dict
    for ind, elem in enumerate(myPerm):

        # mappings[elem] = ind
        mappings[ind] = elem

    for key in range(len(myPerm)):

        # skip all keys that are already included in some cycle
        if not key in mappings:

            continue

        # we're building a new cycle
        cycle = []

        cycle.append(key)

        mapping = mappings[key]

        # remove key from dict here?
        mappings.pop(key)

        while mapping != key:

            cycle.append(mapping)

            next_mapping = mappings[mapping]

            # remove mapping from dict here?
            mappings.pop(mapping)

            mapping = next_mapping

        cycles.append(cycle)

    return cycles
    
p_cycles = getCycles(p)    

# .... now we do the same for A and B; then for each cycle in both A's and B's cycle decomposition, we compute the respective distance between first and 2nd element 

A_cycles = getCycles(A)

B_cycles = getCycles(B)

def get_shifts(base: List[List[int]], cycles: List[List[int]]) -> List[int]:

    shifts = []

    for ind, cycle_ in enumerate(cycles):

        # store first element in the cycle in p
        first_elem = cycle_[0]

        second_elem = None

        # handle 1-element cycles separately
        if len(cycle_) == 1: 

            assert(len(base[ind]) == 1)

            shifts.append(0)

            continue

        else:

            # store first element in the cycle in p
            second_elem = cycle_[1]

        # now find the shift in p for this cycle
        base_cycle = base[ind]

        steps = None

        found = False

        k = 0

        while found == False:

            # print(f"base_cycle: {base_cycle}, cycle_: {cycle_}")

            if base_cycle[k] == first_elem:

                assert(steps == None)

                steps = 0

            elif found == False and steps is not None:

                steps += 1

                if base_cycle[k] == second_elem:

                    found = True

            k = (k + 1) % len(base_cycle)

        # print(f"steps: {steps}")

        shifts.append(steps)

    return shifts

A_shifts = get_shifts(p_cycles, A_cycles)

print(f"Shifts for A: {A_shifts}")

B_shifts = get_shifts(p_cycles, B_cycles)

print(f"Shifts for B: {B_shifts}")

cycle_lengths_p = list(map(lambda x: len(x), p_cycles))

cycle_lengths_a = list(map(lambda x: len(x), A_cycles))

cycle_lengths_b = list(map(lambda x: len(x), B_cycles))

print(f"b_cycles[-5]: {B_cycles[-5]}, p_cycles[-5]: {p_cycles[-5]}")

print(f"Cycle lenghts p: {cycle_lengths_p}, Cycle lengths A: {cycle_lengths_a}, Cycle lengths B: {cycle_lengths_b}")

# remove trivial cycle
cleaned_shifts = []
cleaned_lengths = []

for i in range(len(cycle_lengths_p)):

    if cycle_lengths_p[i] > 1:

        cleaned_shifts.append(A_shifts[i])
        cleaned_lengths.append(cycle_lengths_p[i])

print(f"Cleaned shifts: {cleaned_shifts}, Cleaned lengths: {cleaned_lengths}")

res = crt_generalized(remainders = cleaned_shifts, moduli = cleaned_lengths) 

if res != None:

    gen_crt_sol, mod = res

    print(f"Solution: {gen_crt_sol}, mod = {mod}")

    B_perm = Permutation(B)

    key_Alice = pow(B_perm, gen_crt_sol).to_key()

    # key_Bob = pow(B_perm, sol[0]).to_key()

    cipher = AES.new(key_Alice, AES.MODE_CBC, bytes(16))

    enc_flag = b'8af30997834401a409dc825a104850267d97238ff63097f9a1a0d811acf84a8d2ff280927987f26d2b6c6417220bfee9'

    print(cipher.decrypt(enc_flag).decode(errors="ignore"))