from pprint import pprint
import binascii
import itertools
import string
import binascii
import argparse
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
import os

def randInt(x,y):
    byte = os.urandom(1)
    num = ord(byte)

    calc = y-x+1

    answer = num % calc

    return x + answer

class ecb_cookie_oracle: #modified for week6

    #Server appends secretly.

    def __init__(self,file_name):
        self.random = os.urandom(randInt(10,20)) #Random int from above function!
        self.keys = os.urandom(16)
        self.file = open(file_name,"r").read().decode("base64") #File

    #Give me hex
    def encrypt(self,hx):
        #Py Crypto defaults to ECB
        encryption = AES.new(self.keys)
        s = hx.decode("hex")
        s = self.random + s + self.file
        s = pad(s,128)
        return encryption.encrypt(s)

    #Give me hex
    def decrypt(self,hx):
        #Py Crypto defaults to ECB
        decryption = AES.new(self.keys)
        s = hx.decode("hex")
        s = unpad(s,128)
        return decryption.decrypt(s)

class ecb_oracle:

    def __init__(self):
        self.keys = os.urandom(16)

    #Give me hex
    def encrypt(self,hx):
        #Py Crypto defaults to ECB
        encryption = AES.new(self.keys)
        s = hx.decode("hex")
        s = pad(s,128)
        return encryption.encrypt(s)

    #Give me hex
    def decrypt(self,hx):
        #Py Crypto defaults to ECB
        decryption = AES.new(self.keys)
        s = hx.decode("hex")
        s = unpad(s,128)
        return decryption.decrypt(s)


#Detects if string was encrypted with ecb
def ecb_detect(ascii_string):

    #Breaks into chunks of 16 bytes
    l = split(ascii_string, 16)

    #Loops through to check for ecb using itertools
    for i in itertools.combinations(l,2):
        if i[0] == i[1]:
            return 1

    return 0

#Modified for week5
def ecb_detect_n(ascii_string,n):

    #Breaks into chunks of NX16 bytes
    l = split(ascii_string, 16*n) #Only to find bigger blocks like 32, 48, etc
    sumof = []
    #Loops through to check for ecb using itertools
    for i in itertools.combinations(l,2):
        if i[0] == i[1]:
            return 1

    return 0

#Decrypts a hex string given a key that was used with aes AND ecb mode
def aes_ecb_decrypt(s, k):
    #Py Crypto defaults to ECB
    decryption = AES.new(k)
    s = s.decode("hex")
    return decryption.decrypt(s)

#Decrypts a hex string given a key that was used with aes AND ecb mode
def aes_ecb_encrypt(s, k):
    #Py Crypto defaults to ECB
    encryption = AES.new(k)
    s = s.decode("hex")
    return encryption.encrypt(s)


#Function pads based on block size
def pad(string, block_size):
    padder = padding.PKCS7(block_size).padder()
    data = padder.update(string)
    return data + padder.finalize()


#Function pads based on block size
def unpad(string, block_size):
    unpadder = padding.PKCS7(block_size).unpadder()
    data = unpadder.update(string)
    return data + unpadder.finalize()


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

#Xors string with hex key
def xor2(s,k):
    s = split(s,2)
    k = split(k,2)
    c = itertools.cycle
    x = ''
    for i,j in zip(s,c(k)):
        x += "0x{:02x}".format(int(i,16)^int(j,16))

    return standard(x)


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