# Problem 1

This program will decrypt a cookie like encryption that uses ecb. Currently needs work.

## Getting Started

For this, you need the rypto.py file in the week6 and one.py in the week6 directory.
Also you need a file you wish to decrypt that is currently in base64.

If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one.py

## Assumption

If you don't have these libraries,

    pip install pycrypto
    pip instal cryptography

The counter only goes through 50 iterations. This seemed like plenty. No need to calculate the length added for this assignment. If it doesn't work, add more to the number 50 in the for loop of the c section.

# Problem 2

This program will validate padding of a string with padding and print string without padding

#Getting Started

For this, you need the rypto.py file in the week6 and two.py in the week6 directory.

Running the following command will get you started:

    python two.py

## Assumption

If you don't have these libraries,

    pip install pycrypto
    pip instal cryptography

If a string ends in 1, it must be off by block size or it will go undetected.
So the 'This is a Saturday' example at block size 160 may not be:

'This is a Saturday\x02\x01' because the block size matches and it will go undetected. However, ending in '\x03\x02\x01' would be fine
with 160 bit block size
