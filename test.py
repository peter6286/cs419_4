header_file = open('abc.pow-15', 'r')
for line in header_file:
    # try to find the matching substrings
    if 'INITIAL-HASH: ' in line.upper():
        # find the initial_hash they gave us
        init_given_hash = line[line.index(':') + 2:].strip()
        if not init_given_hash:
            print('No given initial hash')
        # print(line, end='')

    elif 'PROOF-OF-WORK: ' in line.upper():
        work = line[line.index(':') + 2:].strip()
        if not work:
            print("No given work")
        # print(line,end='')

    elif 'HASH: ' in line.upper():
        final_given_hash = line[line.index(':') + 2:].strip()
        if not final_given_hash:
            print('No given hash')
        # print(line,end='')

    elif 'LEADING-BITS: ' in line.upper():
        given_leading = line[line.index(':')].strip()
        if not given_leading:
            print('No given leading bits')
        # print(line,end='')
print(init_given_hash)
