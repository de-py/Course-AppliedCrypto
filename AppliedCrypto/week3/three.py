#!/usr/bin/env python
from cryptography.hazmat.primitives import padding

#Function pads based on block size
def pad(string, block_size):
    padder = padding.PKCS7(block_size).padder()
    data = padder.update(string)
    return data + padder.finalize()


if __name__ == "__main__":


    """
    First Problem
    """

    #Gets phrase to pad
    phrase = "This is a Saturday" #Phrase to bad
    bit_blocks = 160 #paddingBitLength

    #Prints prhase and padding
    print 'Padding for "%s" is: ' % (phrase), repr(pad(phrase, bit_blocks))


    """
    Second Problem (Just erase if not required.)
    """
    #Answer for this problem is in the readme for week3.

    #Gets phrase to pad
    phrase = "NO PAIN NO GAIN!" #Phrase to bad
    bit_blocks = 128 #paddingBitLength

    #Prints prhase and padding
    print 'Padding for "%s" is: ' % (phrase), repr(pad(phrase, bit_blocks))
