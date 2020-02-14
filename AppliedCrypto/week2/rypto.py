from pprint import pprint
import binascii
import itertools
import string
import binascii
import argparse


def file_open():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The input file should contain a b64 string")
    file_name = parser.parse_args().file
    f = open(file_name,'r')
    return f

#Converts base64 string to hex
def b62_hex(s):
    x = s.decode('base64').encode('hex')
    return x
#Pretty prints the frequency of chracters in a string
#Returns most frequent
def freq(s):
    d = {}
    for i in s:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1
    #pprint(d)
    maxv = max(d,key=d.get)
    #pprint(maxv)
    return maxv

#Returns minimum value
def mind(d):

    minv = min(d,key=d.get)

    return minv


#Ascii string to list of hex bytes
def a2hex(word):
    hexed = binascii.hexlify(word)
    l = split(hexed,2)
    empty = []
    for i in l:
        empty.append(hex(int(i,16)))

    return empty


#Splits a string into a list object every n characters
def split(word,n):
    l = []
    for i in range(0,len(word),n):
        l.append(word[i:i+n])
    return l

#Xor a list and a key
def xor(l,k):
    c = itertools.cycle

    xd = []
    for i, j in zip(l,c(k)):
        xd.append("0x{:02x}".format((int(i,16)^int(j,16))))

    return xd

#Removes x's and such
def standard(hex_s):
    if type(hex_s) is str:
        hex_s = hex_s.replace(" ","")
        hex_s = hex_s.replace("0x", "")


    elif type(hex_s) is list:
        hex_s = ''.join(hex_s)
        hex_s = hex_s.replace("0x", "").zfill(2)

    return hex_s


#Convert string to binary
def s2bin(s):
    return ''.join(bin(ord(i))[2:].zfill(8) for i in s)

#Convert hex to binary
def h2bin(h):
    return ''.join(bin(int(i,16))[2:].zfill(8) for i in h)
#Converts to binary and counts differences in bits
def ham(s1, s2):
    if len(s1) == len(s2):
        x = 0
        for i,j in zip(s1,s2):
            if i == j:
                pass
            else:
                x += 1
        return x

    else:
        print "somethings wrong.."
        print s1,s2
