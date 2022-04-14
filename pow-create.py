#!/usr/bin/python3
import hashlib
import math
import sys
import time

hex_dict = {'0': 4, '1': 3, '2': 2, '3': 2, '4': 1, '5': 1, '6': 1, '7': 1, '8': 0, '9': 0, 'a': 0, 'b': 0, 'c': 0,
            'd': 0, 'e': 0, 'f': 0}


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
    a = hex_dict[hash[leading_char_zero]]
    return a >= remaining_zero


def check_leading(nbits, hash):
    # each 0 char is
    leading_char_zero = nbits // 4
    remaining_zero = nbits % 4
    list_zero = ['0'] * leading_char_zero
    for i in range(leading_char_zero):
        if hash[i] != list_zero[i]:
            return False

    latch_zero = hex_dict[hash[leading_char_zero]]
    return latch_zero >= remaining_zero


def get_leading(nbits, hash):
    num_leading = 0
    for char in hash:
        if char != '0':
            break
        num_leading += 4

    return num_leading + hex_dict[hash[num_leading // 4].lower()]


def work_back(work, length):
    go_back = 1
    # loop in reverse
    for idx in range(length, -1, -1):
        # check if at last char
        if work[idx] == chr(126):
            go_back = 1  # 126需要进位
            work[idx] = chr(33)
        else:  # 当前位置的下一位进一位
            go_back = 0
            work[idx] = chr(ord(work[idx]) + 1)
            break

    if go_back == 1:  # 需要进位多加一位length
        work.append(chr(33))
        length += 1

    return work, length


def complment(char,length,work):
    if char > 126:
        char = 33

        for idx in range(length, -1, -1):
            # check if at last char
            if work[idx] == chr(126):
                work[idx] = chr(33)
                if work.index(work[idx]) == 0:
                    work.append(chr(33))
                    length += 1
            else:
                work[idx] = chr(ord(work[idx]) + 1)
                break

    else:
        work[length] = chr(char)
    return work,length


def gen_work(nbits, hash):
    if check_leading(nbits, hash):
        return "", hash, 0

    # 7-bit : 33 - 126
    char = 33
    # has to be a list because strings are immutable
    work = [chr(char)]
    length = 0
    iteration = 1
    new_mes = "".join(work) + hash
    new_hash = get_hash(str.encode(new_mes))
    while not check_leading(nbits, new_hash):
        char += 1
        work, length = complment(char, length, work)
        '''
        work,length = complment(char,length,work)
        if char > 126:

            for idx in range(length, -1, -1):
                # check if at last char
                if work[idx] == chr(126):
                    work[idx] = chr(33)
                    if work.index(work[idx]) == 0:
                        work.append(chr(33))
                        length += 1
                else:
                    work[idx] = chr(ord(work[idx]) + 1)
                    break

        else:
            work[length] = chr(char)
        '''
        new_mes = "".join(work) + hash
        new_hash = get_hash(str.encode(new_mes))
        iteration += 1

    # work, hash, iteration
    return work, new_hash, iteration


def main():
    nbits = int(18)
    file_name = "test.txt"

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
    '''
    if len(sys.argv) != 3:
        print('Please input correct number of args')
        return -1

    # error check for nbits
    try:
        nbits = int(sys.argv[1])
        if nbits < 0:
            print('Please input a proper integer value for nbits')
            return -1
    except:
        print('Please input a proper integer value for nbits')
        return -1

    file_name = sys.argv[2]
    '''
    main()