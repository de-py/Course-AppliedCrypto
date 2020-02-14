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
from struct import *
import hashlib
from operator import mul
import sys
import large_prime
sys.setrecursionlimit(1000000)


class rsa:
    def __init__(self,e):
        self.e = e
        self.p,self.q = find_p_q()
        self.n = self.p*self.q
        self.et = euler(self.p,self.q)
        self.d = mulinv(self.e,self.et)


    #give me ascii
    def enc(self,m):
        # m2 = 'Hi this is short'
        # m2encoded = int(m2.encode("hex"),16)
        # encm2 = rypto.mod_exp(m2encoded,e,n)
        mencoded = int(m.encode("hex"),16)
        return mod_exp(mencoded,self.e,self.n)

    #give me whatever enc returns
    def dec(self,m):
        # hexad = rypto.standard(hex(decm2))
        # decm2b = hexad[:-1].decode("hex")
        decm = mod_exp(m,self.d,self.n)
        hexad = standard(hex(decm))
        return hexad.decode("hex")



#Wikipedia
# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


#Wikipedia
# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def euler(p,q):
    return (p-1)*(q-1)


def find_p_q():
    p = None
    q = None
    while(1):
        print 'Trying to find p..'
        p = large_prime.generateLargePrime(2048)
        if isinstance(p,str):
            pass
        else:
            print 'p found.'
            break;
    while(1):
        print 'Trying to find q..'
        q = large_prime.generateLargePrime(2048)
        if isinstance(q,str):
            pass
        else:
            print 'q found'
            break;
    return p,q





class srp:

    def __init__(self, n, g, k, i, p ): #N = [NIST Prime], g=2, k=3, I (username), P(password)
        self.b = int((os.urandom(256).encode("hex")),16) % n #Hidden value
        self.B = None
        self.n = n
        self.g = g
        self.k = k
        self.i = i
        self.p = p
        self.s = None
        self.v = None
        self.password_db = None
        self.user_auth = None
        self.server_u = None
        self.server_S = None
        self.server_K = None


    def store(self):
        self.s = int((os.urandom(256).encode("hex")),16) % 4294967295 #Random INT
        xH = sha256(str(self.s) + self.p)
        x = int(xH,16)
        self.v = mod_exp(self.g,x,self.n)
        self.password_db = {'i': self.i, 'v': self.v, 's': self.s  }

    def client_send(self,i,A):
        self.user_auth = {'i': i, 'A': A}

    def response(self):
        self.B = (self.k*self.v) + (mod_exp(self.g,self.b, self.n)) #Public B
        return self.s,self.B

    def calc_u(self):
        uH = sha256(str(self.user_auth['A']) + str(self.B))
        self.server_u = int(uH,16)


    def generate_k(self):
        self.server_S = mod_exp(self.user_auth['A']*(mod_exp(self.v,self.server_u,self.n)),self.b,self.n)
        self.server_K = sha256(str(self.server_S))

    def validate(self,user):
        check = sha256(self.server_K + str(self.s))
        if user==check:
            print 'OK'

        else:
            print 'Not-OK'


#Credit to www.math.umn.edu
def mod_exp(x,e,m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X*X) % m
            E = E/2

        else:
            Y = (X * Y) % m
            E = E - 1

    return Y






def sha256(s):
    m = hashlib.sha256()
    m.update(s)
    return m.hexdigest()


class AsciiError(Exception):
    def __init__(self,ascii):
        self.ascii = ascii

    def __str__(self):
        return self.ascii



class cbc_w10:

    def __init__(self):
        self.keys = os.urandom(16)
        self.iv = self.keys

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
            check.decode("ascii")

        except UnicodeDecodeError as e:
            raise AsciiError(check)

        return check






class ctr_mode_sanitize:
    def __init__(self):
        self.key = 'NO PAIN NO GAIN!'
        self.nonce = pack('l',0) # makes bytes like '\x00\x00\x00'

    #These do the same thing
    def encrypt(self,string):
        prepend = 'comment1=raining%20MCs;userdata='
        append = ';comment2=%20like%20a%20sunny%20day%20tomorrow'
        string = sanitizer(string)
        blocks = split(string,16)
        answer = ''
        for i,c in enumerate(blocks):
            counter = pack('l',i) # makes bytes like '\x01\x00\x00'
            both = self.nonce+counter # combintes none and counter
            first = ecb(both,self.key) #First part of encryption
            answer += string_xor(first,c) #XOR each block with each encrypted cunk

        return answer

    #These do the same thing
    def decrypt(self,string):
        blocks = split(string,16)
        answer = ''
        for i,c in enumerate(blocks):
            counter = pack('l',i) # makes bytes like '\x01\x00\x00'
            both = self.nonce+counter # combintes none and counter
            first = ecb(both,self.key) #First part of encryption
            answer += string_xor(first,c) #XOR each block with each encrypted cunk

        return answer

class ctr_mode:
    def __init__(self):
        self.key = 'NO PAIN NO GAIN!'
        self.nonce = pack('l',0) # makes bytes like '\x00\x00\x00'

    #These do the same thing
    def encrypt(self,string):
        blocks = split(string,16)
        answer = ''
        for i,c in enumerate(blocks):
            counter = pack('l',i) # makes bytes like '\x01\x00\x00'
            both = self.nonce+counter # combintes none and counter
            first = ecb(both,self.key) #First part of encryption
            answer += string_xor(first,c) #XOR each block with each encrypted cunk

        return answer

    #These do the same thing
    def decrypt(self,string):
        blocks = split(string,16)
        answer = ''
        for i,c in enumerate(blocks):
            counter = pack('l',i) # makes bytes like '\x01\x00\x00'
            both = self.nonce+counter # combintes none and counter
            first = ecb(both,self.key) #First part of encryption
            answer += string_xor(first,c) #XOR each block with each encrypted cunk

        return answer

def string_xor(s1,s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))



#Slightly modified from before
def ecb(s, k):
    #Py Crypto defaults to ECB
    encryption = AES.new(k, AES.MODE_ECB)
    return encryption.encrypt(s)


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


#Xors string with hex key
def xor2(s,k):
    s = split(s,2)
    k = split(k,2)
    c = itertools.cycle
    x = ''
    for i,j in zip(s,c(k)):
        x += "0x{:02x}".format(int(i,16)^int(j,16))

    return standard(x)


#Removes x's and such
def standard(hex_s):
    if type(hex_s) is str:
        #print hex_s
        hex_s = hex_s.replace(" ","")
        hex_s = hex_s.replace("0x", "").zfill(2).replace('L','')
        if len(hex_s) % 2 != 0:
            hex_s = '0' + hex_s


    elif type(hex_s) is list:
        hex_s = ''.join(hex_s)
        hex_s = hex_s.replace("0x", "").zfill(2)

    return hex_s



