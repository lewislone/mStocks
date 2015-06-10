#coding: UTF-8

abc=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'A']

def nu2abc(nu):
    ab='' 
    l = len(abc) - 1
    remain = nu + 1 
    while remain:
       left = remain % l
       remain = remain / l
       ab = abc[left - 1] + ab

    return ab

if __name__ == '__main__':
    print len(abc)
    print nu2abc(12083)
    print nu2abc(26)
