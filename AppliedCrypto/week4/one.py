#!/usr/bin/env python
import rypto
from pprint import pprint
from Crypto.Cipher import AES

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

#Actual decrypting
def cbc_decrypt(s,k,iv):

    #Decryption of block
    block = rypto.aes_ecb_decrypt(s,k)

    #Encode
    block =  block.encode("hex")

    #xor block1 hex with iv (already in hex)
    xored =  rypto.xor2(block,iv)

    return xored


def short_open(filename):
    #Open file
    f = open(filename,"r") #Change w4p1.txt to your file. Must be a single b64 line.

    #Read first line
    b64 = f.read()

    #Convert base64 to hex
    hx = rypto.b62_hex(b64)

    return hx



#Main Function
if __name__ == "__main__":

    #File to b64 to hex
    hx = short_open("w4p1.txt") #Filename = w4p1.txt

    #IV
    iv = '00000000000000000000000000000000' #iv

    #Key (In ascii)
    ascii_key = 'NO PAIN NO GAIN!' #key in Ascii, DONT CHANGE

    #Block size
    bs = 128 #Padding block size

    #Convert ascii key into hex string
    hex_string_key = ascii_key.encode("hex") #AESKeyToChange (Replace everything after the '='s)
    hex_string_key = rypto.standard(hex_string_key) #Standardizes key to best of ability

    """
    Please read assumption about this key. If all assumptions are thrown away,
    remove second hex_string_key line and end with first ascii-like input with
    encoding hex_string_key as hex. That should work. " ".encode("hex")
    """

    #Magic
    print prep_cbc(hx,hex_string_key, iv, bs)
