#!/usr/bin/env python
import rypto


if __name__ == "__main__":
    user_data = 'This|Is|A|Long|Arbitrary|;String;"ADMIN=FALSE";|I|Though|I|Would|Add|RANDOM'


    func = rypto.ctr_mode_sanitize() #CTR function

    enc = func.encrypt(user_data) #Encrypted data
    dec = func.decrypt(enc) #Decrypted data

    print 'Original decryption:\r\n', dec

    print "Checking if decryption contains the value \";admin=true;\" ..."
    print rypto.checker(dec)
    print

    block_num = 3
    print "Attempting to change block number " + str(block_num) + "\n"

    splt = rypto.split(enc,16) #Split to blocks

    splt[block_num-1] = ';admin=true;XXXX' #Add my own block

    try_one = ''.join(splt) #Join list to decrypt

    decrypted_result = func.decrypt(try_one) #Get this value and store

    splt2 = rypto.split(decrypted_result,16) #Break up stored value to blocks

    splt_new = splt2[block_num-1] #Take result from same location and store

    splt[block_num-1] = splt_new #Put into same location of original encrypted

    try_again = ''.join(splt2) #Join data again with new value in place

    decrypted = func.decrypt(try_again) #Decrypt the new string again with proper xor'd value this time

    print decrypted

    print "Checking if decryption contains the value \";admin=true;\" ..."
    print rypto.checker(decrypted)
    print


