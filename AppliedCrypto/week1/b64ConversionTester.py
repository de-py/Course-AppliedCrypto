#!/usr/bin/env python
from hex2Base64 import hex2b64, standardize
import argparse
import binascii
from time import sleep

def file_open():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The input file should contain hex strings, one on each line")
    file_name = parser.parse_args().file
    f = open(file_name,'r')
    return f

def check(x):
    theirs = binascii.b2a_base64(x.decode("hex"))
    theirs = theirs.replace('\n','')
    mine = hex2b64(x)
    if mine == theirs:
        return True
    else:
        return False

if __name__ == '__main__':
    f = file_open()
    lines = f.readlines()
    for i in lines:
        x = i.replace('\n','')
        x = standardize(x)
        print 'Checking ' + x
        sleep(1)
        print check(x)
        sleep(1)
