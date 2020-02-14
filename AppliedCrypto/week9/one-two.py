#!/usr/bin/env python
import rypto


if __name__ == "__main__":
    b64 = open("w9enc.txt").read() #Read in file
    enc = b64.decode("base64") #Decode base64 = encrypted text

    func = rypto.ctr_mode() #CTR function

    a = func.decrypt(enc)

    print 'Decrypted:\r\n', a

    b = func.encrypt(a)

    print 'Encrypted (in hex)\r\n', b.encode("hex")
    print

    print 'Original encryption (in hex)\r\n', enc.encode("hex")




