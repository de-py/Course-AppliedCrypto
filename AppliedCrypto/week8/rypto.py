from pprint import pprint
import binascii
import itertools
import string
import binascii
import argparse
#from CCipher import AES
from cryptography.hazmat.primitives import padding
import os
from Crypto.Cipher import AES

class webapp:

    def __init__(self):
        self.keys = os.urandom(16)
        self.iv = os.urandom(16)

    #Give me ascii
    def encrypt(self,user_input):
        clean_user_input = pad(user_input,128)
        clean_user_input = clean_user_input.encode("hex")
        return enc_cbc(clean_user_input,self.keys,self.iv)


    #Give me ascii
    def decrypt(self,user_encrypted):
        hx = user_encrypted.encode("hex")
        check = cbc_nounpad(hx,self.keys,self.iv,128) #Decrypts without unpadding

        try:
            if is_padding(check,128):
                return True,check
        except:
            return False,check



#Example \x02 as last byte should be \x03\x03\x03 and not \x03\x03\x01
def same_byte_check(hx,num_bytes):

    if len(set(hx[-num_bytes:])) == 1: #If last bytes in list are all the same
        pass
    else:
        raise ValueError('The padding bytes are not all the same')

#Checks against default padding function. Helpful to confirm block_size check
def block_size_check(b_string, block_size):
    try:
        unpad(b_string,block_size)

    except Exception:
        raise ValueError('The padding bytes do not match the block size')

def is_padding(the_string, block_size):
    hx = the_string.encode("hex")
    hx = split(hx,2)
    last = hx[-1] #Last byte in string
    num_bytes = int(last,16)

    if num_bytes == 1:
        block_size_check(the_string,block_size) #Checks to make sure valid to block size
        #print 'Assuming it is ACTUALLY only padded with one byte:' #If it made it past block size check
        return unpad(the_string,block_size)

    else:
        try:
            same_byte_check(hx,num_bytes) #Checks for ending in correct number of bytes and the same byte
            block_size_check(the_string,block_size)#Checks again blocksize with default padding function
            return unpad(the_string,block_size)#Returns block size with assumption it made it this far without errors
        except ValueError as e:
            raise



def cbc_nounpad(s,k,iv,bs):

    iv = iv.encode("hex")

    final = ''
    #Splits into 16 byte blocks
    s = split(s,32)
    #print s

    #Converts to ascii, kinda. Just required of AES function.
    #k = k.decode("hex")

    #Inserts iv to the beginning of the block for the for loop
    s.insert(0,iv)

    #Cycle through all blocks
    for i in range(1,len(s)):
        x = cbc_decrypt(s[i],k,s[i-1]) #Decrypts and sends iv as s[i-1]
        final += x.decode("hex") #Decodes reponse


    return final #Unpads and returns



class week7_encrypt:

    def __init__(self):
        self.keys = os.urandom(16)
        self.iv = os.urandom(16)

    #Give me ascii
    def encrypt(self,user_input):
        clean_user_input = sanitizer(user_input)
        clean_user_input = pad(clean_user_input,128)
        clean_user_input = clean_user_input.encode("hex")
        return enc_cbc(clean_user_input,self.keys,self.iv)


    #Give me ascii
    def decrypt(self,user_encrypted):
        hx = user_encrypted.encode("hex")
        return prep_cbc(hx,self.keys,self.iv,128)





def checker(decrypted):
    checked = ';admin=true;'
    if checked in decrypted:
        return True

    else:
        return False




#k = key, s = hex string to encrypt, iv = iv, bs = block size
def enc_cbc(s,k,iv):

    final = ''

    #Splits into 16 byte blocks
    s = split(s,32)


    #Cycle through all blocks
    for i in range(0,len(s)):
        iv = cbc_encrypt(s[i],k,iv) #Encrypts and sends iv as s[i-1]
        final += iv


    return final #Returns



#Actual decrypting
def cbc_decrypt(s,k,iv):


    #Decryption of block
    block = aes_ecb_decrypt(s,k)

    #Encode
    block =  block.encode("hex")

    #xor block1 hex with iv (already in hex)
    xored =  xor2(block,iv)

    return xored

#k = key, s = hex string to decrypt, iv = iv, bs = block size
def prep_cbc(s,k,iv,bs):

    iv = iv.encode("hex")

    final = ''
    #Splits into 16 byte blocks
    s = split(s,32)

    #Converts to ascii, kinda. Just required of AES function.
    #k = k.decode("hex")

    #Inserts iv to the beginning of the block for the for loop
    s.insert(0,iv)

    #Cycle through all blocks
    for i in range(1,len(s)):
        x = cbc_decrypt(s[i],k,s[i-1]) #Decrypts and sends iv as s[i-1]
        final += x.decode("hex") #Decodes reponse


    return unpad(final,bs) #Unpads and returns

#Actual encrypting
def cbc_encrypt(b,k,iv):

    iv = iv.encode("hex")
    #Xor block with key
    xored = xor2(b,iv)

    #Encryption of block
    block = aes_ecb_encrypt(xored,k)

    return block


def sanitizer(dirty):
    prepend = 'comment1=raining%20MCs;userdata='
    append = ';comment2=%20like%20a%20sunny%20day%20tomorrow'
    dirty = prepend + dirty + append
    clean = dirty.replace(';','').replace('=','')
    return clean





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