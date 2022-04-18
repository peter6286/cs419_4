#!/usr/bin/python3
import sys
import hashlib

hex_dict = {'0': 4, '1': 3, '2': 2, '3': 2, '4': 1, '5': 1, '6': 1, '7': 1, '8': 0, '9': 0, 'a': 0, 'b': 0, 'c': 0,
            'd': 0, 'e': 0, 'f': 0}


def get_hash(str):
    m = hashlib.sha256()
    # m.update(bytes(str, 'utf-8')) # I did this when reading it in as r instead of rb mode
    m.update(str)
    return m.hexdigest()


def get_leading(hash):
    num_leading = 0
    for char in hash:
        if char != '0':
            break
        num_leading += 4

    return num_leading + hex_dict[char.lower()]


def main():
    if len(sys.argv) != 3:
        print('Please input correct number of args')
        return -1

    header_file_name = sys.argv[1]
    text_file_name = sys.argv[2]

    header_file = open(header_file_name, 'r')
    text_file = open(text_file_name, 'rb')

    if not header_file:
        print('File cannot open')
        return -1
    if not text_file:
        print('File cannot open')
        return -1

    # parse file line by line
    for line in header_file:
        # try to find the matching substrings
        if 'INITIAL-HASH: ' in line.upper():
            # find the initial_hash they gave us
            header_init = line[line.find(':') + 2:].strip()
            # print(line, end='')

        elif 'PROOF-OF-WORK: ' in line.upper():
            header_work = line[line.find(':') + 2:].strip()
            # print(line,end='')

        elif 'HASH: ' in line.upper():
            header_hash = line[line.find(':') + 2:].strip()
            # print(line,end='')

        elif 'LEADING-BITS: ' in line.upper():
            header_leading = line[line.find(':') + 2:].strip()
            # print(line,end='')

    # check if each of the 4 things we need exist
    if not header_init:
        print('No given initial hash')
        return -1

    if not header_work:
        print("No given work")
        return -1

    if not header_hash:
        print('No given hash')
        return -1

    if not header_leading:
        print('No given leading bits')
        return -1

    '''

    if init_calc_hash != init_given_hash:
        print('Initial hash does not match')
        return -1
    '''
    # calculate final hash
    init_mes = text_file.read()
    text_hash = get_hash(init_mes)
    final_mes = text_hash + header_work
    final_calc_hash = get_hash(str.encode(final_mes))

    if header_init != text_hash :
        print('ERROR: inital hashes do not match \n')
        print('hash in header: {}'.format(header_init))
        print('file hash: {}'.format(text_hash))

        # calc num leading bits
        calc_leading = get_leading(final_calc_hash)
        # need to try to cast leading bits to int
        try:
            given_leading = int(header_leading)
        except ValueError:
            print('Given leading bits is not a valid num')
            return -1

        if calc_leading != given_leading:
            print('Leading bits does not match')
            return -1

    if final_calc_hash != header_hash:
        print('ERROR: pow hash does not match Hash header \n')
        print('expected: {}'.format(final_calc_hash))
        print('header has: {}'.format(text_hash))

    print('pass')
    return 0


if __name__ == "__main__":
    main()