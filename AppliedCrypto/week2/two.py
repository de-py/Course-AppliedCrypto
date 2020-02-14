#!/usr/bin/env python
import rypto
from pprint import pprint


#Stores hamming distance results in a dictionary, returns dictionary
def ave_ham(s):
    d = {}
    for i in xrange(1,46):
        n = i*8
        d[i] = adj_ham(s,n)

    return d

#Compares adjancent hamming distances of n chunks and returns average
def adj_ham(l,n):
    l = rypto.split(l,n)
    x = 0
    count = 0
    for i, j in zip(l, l[1:]):
        if len(i) == len(j):
            x += rypto.ham(i,j)/float(n/8)
            count += 1
        else:
            pass
    return x/float(count)

#Splits a string into blocks of a given number
def blocks(s,n):
    l = []
    for i in range(n):
        l.append(s[i::n])
    return l

if __name__ == "__main__":
    #Opens a file, converts string to hex, properly formatted
    f = rypto.file_open()
    f = f.read()
    f = rypto.b62_hex(f)
    f =  rypto.split(str(f),2)

    #Determines the average hamming distance
    d = ave_ham(rypto.h2bin(f))

    print 'Average hamming distances:'
    pprint(d)

    #Pull minimum value from dictionary and gives key of that which is
    #Key length
    keylength = rypto.mind(d)
    print
    print 'Key Length is: ', keylength
    print

    #Breaks list of hex bytes into blocks given the key length
    l = (blocks(f,keylength))

    #Determines most used hex byte, appends to list k.
    k = []
    for i in l:
        k.append(rypto.freq(i))

    print 'Key could be:', ''.join(k).decode("hex")

    print


    #Xors each most used byte with the most used character (Space)
    s = []

    for i in k:
        s.append("0x{:02x}".format(int(i,16)^ord(' ')))

    #Changes hex to correct format for being xored.
    s = rypto.standard(s)
    s = rypto.split(s,2)

    #Xors the key with the original hex bytes, standardizes answer, and decodes the hex bytes
    print rypto.standard(rypto.xor(f,s)).decode("hex")
