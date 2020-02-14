#!/usr/bin/env python
import rypto
from pprint import pprint
from Crypto.Cipher import AES

#Decrypts a hex string given a key that was used with aes AND ecb mode
def aes_ecb_decrypt(s, k):
    #Py Crypto defaults to ECB
    decryption = AES.new(k)
    s = s.decode("hex")
    return decryption.decrypt(s)


#Main Function
if __name__ == "__main__":
    #Open file and read first line
    f = rypto.file_open().read()

    #Converts b64 to hex
    hex_string = rypto.b62_hex(f)

    #Gets key from user
    aes_key = "5NQdRr6sjjkFnHSAOvAVeg==".decode("base64") #AESKEYToChange

    #Decrypts with key and hex string
    answer =  aes_ecb_decrypt(hex_string,aes_key)

    #Prints the answer
    print answer
