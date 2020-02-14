#!/usr/bin/env python
import rypto
from pprint import pprint

if __name__ == "__main__":

    #a = "We didn't start the fire, It was always burning, Since the world's been turning, We didn't start the fire, No we didn't light it, But we tried to fight it"
    a = raw_input("Please enter a phrase to encrpt: ")
    b = raw_input("Please enter a key to encrypt with:")
    #Turning the strings into a list of hex bytes
    line = rypto.a2hex(a)
    key = rypto.a2hex(b)

    #Pretty printing these lists
    #pprint(key
    #pprint(line)

    #print("%s repeatedly xored with %s equals: \n" % (' '.join(key), ' '.join(line)))


    answer = rypto.xor(line,key)

    print rypto.standard(''.join(answer))
