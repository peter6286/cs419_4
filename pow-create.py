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
    return count


def sha256(str):
    m = hashlib.sha256()
    m.update(str)
    return m.hexdigest()


def check_zero(nbits, hash):
    leading_char_zero = nbits // 4
    generate = ['0' for _ in range(leading_char_zero)]
    if hash[:leading_char_zero] != ''.join(generate):
        return False

    remaining_zero = nbits % 4
    return checkzero(hash[leading_char_zero]) >= remaining_zero


def leading(hash):
    num_leading = 0
    for char in hash:
        if char != '0':
            break
        num_leading += 4

    return num_leading + checkzero(hash[num_leading // 4].lower())


def implment(work):
    for idx in range(0, len(work)):
        if work[idx] == chr(126):
            if idx == len(work) - 1:
                work.append(chr(33))
            work[idx] = chr(33)
        else:
            work[idx] = chr(ord(work[idx]) + 1)
            break
    return work


def getworkk(fits, hash):
    if check_zero(fits, hash):
        return "", hash, 0
    char = 33
    work = [chr(char)]
    count = 1
    new_mes = hash + "".join(work)
    new_hash = sha256(str.encode(new_mes))
    while not check_zero(fits, new_hash):
        work = implment(work)
        new_mes = hash + "".join(work)
        new_hash = sha256(str.encode(new_mes))
        count += 1
    return new_hash,work,count


def main(difficulty,file):
    fits = difficulty
    file_name = file

    f = open(file_name, 'rb')
    if not f:
        exit('File cannot open')
    mes = f.read()

    initial_hash = sha256(mes)

    start = time.time()
    new_hash,work,count = getworkk(fits, initial_hash)
    compute_time = time.time() - start
    leanings = leading(new_hash)

    # outputs
    print('File: {}'.format(file_name))
    print('Initial-hash: {}'.format(initial_hash))
    print('Proof-of-work: {}'.format("".join(work)))
    print('Hash: {}'.format(new_hash))
    print('Leading-bits: {}'.format(leanings))
    print('Iterations: {}'.format(count))
    print('Compute-time: {}'.format(compute_time))

    f.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit('Please input correct number of args')

        # error check for nbits
    try:
        difficulty = int(sys.argv[1])
        if difficulty < 0 :
            exit('Please input a proper integer value for nbits')
    except:
        exit('Please input a proper integer value for nbits')

    file_name = sys.argv[2]
    main(difficulty,file_name)
