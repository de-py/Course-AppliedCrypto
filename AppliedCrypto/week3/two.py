#!/usr/bin/env python
import rypto
from pprint import pprint
import itertools


#Detects if string was encrypted with ecb
def ecb_detect(hex_string):

    #Breaks into chunks of 16 bytes
    l = rypto.split(hex_string,16)

    #Loops through to check for ecb using itertools
    for i in itertools.combinations(l,2):
        if i[0] == i[1]:
            return 1

    return 0

if __name__ == "__main__":
    #Open file and read all lines
    f = rypto.file_open().readlines()
    line = []

    #Loops through each line
    for i in range(len(f)):

        #Checks the string for similar values
        if ecb_detect(f[i]) == 1:
            line.append(i+1)

    print 'ECB was detected on these lines: ', line
