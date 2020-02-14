#!/usr/bin/env python
import rypto


if __name__ == "__main__":
    url = 'https://www.google.com/culturalinstitute/beta/u/0/' #The url

    ryp = rypto.cbc_w10() #Calling oracle
    enc = ryp.encrypt(url)#Encrypting with oracle



    enc_split = rypto.split(enc,16) #Breaking into blocks




    evil_enc = enc_split[0] + "\x00"*16 + enc_split[0] #Attacker modifies encypted



    error_capture = None #Sets up for try statement



    try:
        print ryp.decrypt(evil_enc) #If this works, print it out (This should never occur)

    except rypto.AsciiError as e: #If hits (custom) error, capture response from server
        error_capture =  str(e)



    error_split = rypto.split(error_capture,16) #Break error response into blocks



    the_key = rypto.string_xor(error_split[0],error_split[2]) #Pull out the key by xor p1 with p3


    print 'Evil attacker key: ' +  the_key.encode("hex") #Attacker value
    print 'Private original key: ' + ryp.keys.encode("hex")#Machine value (Normally not available)


