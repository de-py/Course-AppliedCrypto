#!/usr/bin/env python
from hex2Base64 import hex2b64, standardize, make_bin_2, make_upper, make_hex
from time import sleep


#XORS binary string of same length
def xor(a,b):
    if len(a) == len(b):
        x = ''
        for i,j in zip(a,b):
            x += str(int(i)^int(j))

        return x
    else:
        print "A and B are not the same length"
        sleep(1)
        print "Exiting..."
        sleep(1)
        exit()

#Prepares input for XOR by normalizing it and converting to binary       
def prep_input(value):
    value = standardize(value)
    value = make_upper(value)
    value = make_bin_2(value)

    return value

#Xors two hex strings. Returns upper case hex values
def xor_me(a,b):
    a = prep_input(a)
    b = prep_input(b)
    xored = xor(a,b)
    x = make_hex(xored)
    return x

if __name__ == '__main__':
    a = raw_input("Input a: ")
    b = raw_input("Input b: ")
    x = xor_me(a,b)

    print "Output: ",x
