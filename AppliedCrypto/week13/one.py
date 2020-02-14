#!/usr/bin/env python
import rypto
import sys
import large_prime
sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)






def main():
    e = (2**16)+1
    client = rypto.rsa(e) #RSA class
    secret = 'secret text' #Secret text (hidden from attacker)
    enc_sec = client.enc(secret) #Encrypted text (Known by attacker)
    known = pow(30,e) #Attacker picks a known value of their own
    hidden = (known*enc_sec) % client.n #Attacker hides value using multiplication
    dec_hidden = client.dec(hidden) #Decrypt attack value (passes check of server)

    x = int(dec_hidden.encode("hex"),16)/30 #Divide attacker known value
    x = rypto.standard(hex(x)).decode("hex") #Convert and such
    print x 

    
    

if __name__ == "__main__":
    main()

