#!/usr/bin/python3
import sys
import hashlib

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


def get_leading(hash):
    num_leading = 0
    for char in hash:
        if char != '0':
            break
        num_leading += 4

    return num_leading + checkzero(char.lower())

def checkhash(text_hash,header_hash):
    if header_hash != text_hash :
        print('ERROR: inital hashes do not match ')
        print('hash in header: {}'.format(header_hash))
        print('file hash: {}'.format(text_hash))
    else:
        print('PASSED: inital file hashes match')
        return True
    return False

def checkleading(text_hash,work,leading):
    final_mes = text_hash + work
    final_calc_hash = sha256(str.encode(final_mes))
    calc_leading = get_leading(final_calc_hash)
    try:
        given_leading = int(leading)
    except ValueError:
        print('Given leading bits is not a valid num')

    if calc_leading != given_leading:
        print('ERROR: incorrect Leading-bits value:{} ,expected {}'.format(given_leading,calc_leading))
    else:
        print('PASSED: leading bits is correct')
        return True
    return False


def checkwork(text_hash,work,header_hash):
    final_mes = text_hash + work
    final_calc_hash = sha256(str.encode(final_mes))
    if final_calc_hash != header_hash:
        print('ERROR: pow hash does not match Hash header')
        print('expected: {}'.format(final_calc_hash))
        print('header has: {}'.format(header_hash))
    else:
        print("PASSED: hash matches Hash header")
        return True
    return False


def process(header_init,header_work,header_hash,header_leading,init_mes):

    text_hash = sha256(init_mes)
    initcheck = checkhash(text_hash,header_init)
    leadcheck = checkleading(text_hash, header_work, header_leading)
    workcheck = checkwork(text_hash,header_work,header_hash)


    if initcheck and leadcheck and workcheck:
        print('pass')
    else:
        print("fail")

def readfile(header,text):
    readh = open(header, 'r')
    readt = open(text, 'rb')
    fileinit = fileproof = filehash = fileleading = False
    if not readh:
        exit('File cannot open')
    if not readt:
        exit('File cannot open')

    for line in readh:
        if 'INITIAL-HASH: ' in line.upper():
            header_init = line[line.index(':') + 2:].strip()
            fileinit = True

        elif 'PROOF-OF-WORK: ' in line.upper():
            header_work = line[line.index(':') + 2:].strip()
            fileproof = True


        elif 'HASH: ' in line.upper():
            header_hash = line[line.index(':') + 2:].strip()
            filehash = True


        elif 'LEADING-ZERO-BITS: ' in line.upper():
            header_leading = line[line.index(':') + 2:].strip()
            fileleading = True

    if not fileinit:
        exit('No given initial hash')

    if not fileproof:
        exit("No given work")

    if not filehash:
        exit('No given hash')

    if not fileleading:
        exit('No given leading bits')

    init_mes = readt.read()

    return header_init, header_work, header_hash, header_leading, init_mes


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit('Please input correct number of args')
    header = sys.argv[1]
    text = sys.argv[2]
    header_init, header_work, header_hash, header_leading, init_mes = readfile(header,text)
    process(header_init, header_work, header_hash, header_leading, init_mes)