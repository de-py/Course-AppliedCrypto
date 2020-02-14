#!/usr/bin/env python
import rypto
from pprint import pprint
from Crypto.Cipher import AES
import os

#Preps cbc decryption
#k = key, s = hex string to decrypt, iv = iv, bs = block size
def prep_cbc(s,k,iv,bs):

    final = ''
    #Splits into 16 byte blocks
    s = rypto.split(s,32)

    #Converts to ascii, kinda. Just required of AES function.
    k = k.decode("hex")

    #Inserts iv to the beginning of the block for the for loop
    s.insert(0,iv)

    #Cycle through all blocks
    for i in range(1,len(s)):
        x = cbc_decrypt(s[i],k,s[i-1]) #Decrypts and sends iv as s[i-1]
        final += x.decode("hex") #Decodes reponse


    return rypto.unpad(final,bs) #Unpads and returns

#k = key, s = hex string to encrypt, iv = iv, bs = block size
def enc_cbc(s,k,iv):

    final = ''

    #Splits into 16 byte blocks
    s = rypto.split(s,32)


    #Cycle through all blocks
    for i in range(0,len(s)):
        iv = cbc_encrypt(s[i],k,iv) #Encrypts and sends iv as s[i-1]
        final += iv


    return final #Returns




#Actual encrypting
def cbc_encrypt(b,k,iv):

    iv = iv.encode("hex")
    #Xor block with key
    xored = rypto.xor2(b,iv)

    #Encryption of block
    block = rypto.aes_ecb_encrypt(xored,k)

    return block


#Actual decrypting
def cbc_decrypt(s,k,iv):


    #Decryption of block
    block = rypto.aes_ecb_decrypt(s,k)

    #Encode
    block =  block.encode("hex")

    #xor block1 hex with iv (already in hex)
    xored =  rypto.xor2(block,iv)

    return xored


#Generate random integer between x and y, including x and y.
def randInt(x,y):
    byte = os.urandom(1)
    num = ord(byte)

    calc = y-x+1

    answer = num % calc

    return x + answer



#Main Function
if __name__ == "__main__":

    #Open file
    f = open("w4p2.txt","r").read() #inputFile

    #Generate random key
    key_rand = os.urandom(16)

    #Generate random iv
    iv = os.urandom(16)

    #Chooses number between 5 and 10
    prependNum = randInt(5,10) #NoOfPrependBytes
    appendNum = randInt(5,10) #NoOfAppendBytes

    prependBytes = os.urandom(prependNum)
    appendBytes = os.urandom(appendNum)

    #Adds bytes to f
    f = prependBytes + f + appendBytes

    #Adds padding to f
    f = rypto.pad(f,128)

    #Convert acsii to hex
    hx = f.encode("hex")

    #Chooses number between 1 and 2 to decide ecb or cbc
    choice = randInt(1,2) #randomChoiceOfECB-CBC (1 = ecb), (2 = cbc)

    if choice == 1:
        print "ECB mode selected"
        x = rypto.aes_ecb_encrypt(hx,key_rand)

    if choice == 2:
        print "CBC mode selected"
        x = enc_cbc(hx,key_rand,iv)

    #Checks for ecb
    result =  rypto.ecb_detect(x.encode("hex"))

    if result == 1:
        print '\nThis was likely encrypted with ecb'

    else:
        print '\nThis was likely encrypted with cbc'





    while(1):
        print '\nType 1 to view result in hex.\nType 2 to view result as is.'
        print 'Type 3 to view result in base64\nType 4 to exit'
        z = int(raw_input("\nYour choice:"))
        if z == 1:
            print x.encode("hex")

        if z == 2:
            print x

        if z == 3:
            print x.encode("base64")

        if z == 4:
            exit()

