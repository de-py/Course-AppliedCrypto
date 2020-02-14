#!/usr/bin/env python
from hex2Base64 import split_stuff, hex2b64, standardize
from xor_func import xor_me
from pprint import pprint
from time import sleep


#counts number of times and prints nicely
def freq(l):
    d = {}
    for i in l:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1

    pprint(d)



if __name__ == '__main__':
    f = open("p3.txt","r")
    f = f.read().replace('\n','')
    
    x = split_stuff(f,2)

    freq(x)

    new = []
    for i in x:
        new.append(xor_me(i,'4f'))

    #print new
    
    print ''.join(new).decode("hex")
    #freq(new)

    new2 = []
    #for i in x:
    #    new2.append(xor_me(i, '00'))

    #print ''.join(new2)
