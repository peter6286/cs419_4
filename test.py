
def work_back2(work, length):

    for idx in range(0,len(work)):
        if work[idx] == chr(126):
            if idx == len(work)-1:
                work.append(chr(33))
                length +=1
            work[idx] = chr(33)
        else:
            work[idx] = chr(ord(work[idx]) + 1)
            break



    return work, length


print(work_back2(['!','!'],1) )