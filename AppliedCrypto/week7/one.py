#!/usr/bin/env python
import rypto


#Main Function
if __name__ == "__main__":
    user = 'Thisisalot;admin=true;' #Arbitrary Data
    ryp = rypto.week7_encrypt() #Create encrypt class
    enc = ryp.encrypt(user) #Encrypt Arbitrary Data



    splt = rypto.split(enc,16) #Split into blocks

    print "Original decryption =:\n" + ryp.decrypt(enc) + "\n"

    print "Checking if decryption contains the value \";admin=true;\" ..."
    print rypto.checker(ryp.decrypt(enc))
    print

    block_num = 2 #Block number to change beginning with block 2

    print "Attempting to change block number " + str(block_num) + "\n"


    splt[block_num-2] = ';admin=true;XXXX' #Set first block to my values

    dec = ryp.decrypt(''.join(splt)) #Decrypt the block with my new values

    print "Middle-step decryption =:\n" + dec + "\n"

    splt_dec = rypto.split(dec,16) #Split up the decrypted blocks again


    mine = splt_dec[block_num-1] #Pull the second block, the first one affected by my change

    splt[block_num-2] = mine #Make the original encrypted block the block we just pulled because (XOR)

    dec = ryp.decrypt(''.join(splt)) #(Decrypt the final modified version)

    print "Final decryption =:\n" + dec + "\n"
    print "Checking if decryption contains the value \";admin=true;\" ..."
    print rypto.checker(dec)