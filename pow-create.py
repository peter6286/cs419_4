#!/usr/bin/python3
import hashlib
import sys
import time
def checkzero(str):
    a = int(str, 16)
    bnr = bin(a).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 4:
        x += '0'
    bnr = x[::-1]
    count = 0
    for item in bnr:
        if item == '1':
            return count
        elif item == '0':
            count += 1

def get_hash(str):
    m = hashlib.sha256()
    # m.update(bytes(str, 'utf-8')) # I did this when reading it in as r instead of rb mode
    m.update(str)
    return m.hexdigest()

def check_leading2(nbits, hash):
    # each 0 char is
    leading_char_zero = nbits // 4
    if hash[:leading_char_zero] != ''.join(['0' for _ in range(leading_char_zero)]):
        return False

    remaining_zero = nbits % 4
    # a = hex_dict[hash[leading_char_zero]]
    return checkzero(hash[leading_char_zero]) >= remaining_zero



def get_leading(nbits, hash):
    num_leading = 0
    for char in hash:
        if char != '0':
            break
        num_leading += 4

    return num_leading + checkzero(hash[num_leading // 4].lower())

def work_back2(work):
    for idx in range(0,len(work)):
        if work[idx] == chr(126):
            if idx == len(work)-1:
                work.append(chr(33))
            work[idx] = chr(33)
        else:
            work[idx] = chr(ord(work[idx]) + 1)
            break
    return work


def gen_work(nbits, hash):
    if check_leading2(nbits, hash):
        return "", hash, 0

    # 7-bit : 33 - 126
    char = 33
    # has to be a list because strings are immutable
    work = [chr(char)]
    iteration = 1
    new_mes = hash + "".join(work)
    new_hash = get_hash(str.encode(new_mes))
    while not check_leading2(nbits, new_hash):
        work = work_back2(work)
        new_mes = hash + "".join(work)
        new_hash = get_hash(str.encode(new_mes))
        iteration += 1

    # work, hash, iteration
    return work, new_hash, iteration


def main():
    nbits = int(20)
    file_name = "trees.jpg"

    # error check for file
    f = open(file_name, 'rb')
    if not f:
        print('File cannot open')
        return -1
    mes = f.read()

    initial_hash = get_hash(mes)

    start = time.time()
    work, new_hash, iterations = gen_work(nbits, initial_hash)
    compute_time = time.time() - start

    # I could calculate the number of leading 0s during it but that might add time
    leading = get_leading(nbits, new_hash)

    # outputs
    print('File: {}'.format(file_name))
    print('Initial-hash: {}'.format(initial_hash))
    print('Proof-of-work: {}'.format("".join(work)))
    print('Hash: {}'.format(new_hash))
    print('Leading-bits: {}'.format(leading))
    print('Iterations: {}'.format(iterations))
    print('Compute-time: {}'.format(compute_time))

    f.close()


if __name__ == "__main__":
    main()