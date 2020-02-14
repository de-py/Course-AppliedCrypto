# Problem 1

This program will decrypt p1.txt, the base64 encoded file, given a key.


## Getting Started

For this, you only need the rypto.py file in the week3 and one.py in the week3 directory.
Also you need a file you wish to decrypt that is currently in base64.

Running the following command will get you started:

    python one.py filename


## Assumptions

You have the directory cloned, your file is base64. Pycrypto is installed.

    pip install pycrypto

# Problem 2

This program determines the line number of the hex string that was encrypted with aes ecb mode.

## Getting started

For this, you only need the rypto.py file in the week3 and two.py in the week3 directory.
Also you need a file with different lines in hex to detect ecb.

Running the following command will get you started:

    python two.py filename

## Assumptions

You have the directory cloned, your file is in hex. Pycrypto is installed. The text file is the same hex formatting as the test file originally.

    pip install pycrypto


# Problem 3

This program pads a string with the amount of blocks you specify.

## Getting started

For this, you only need three.py.

Running the following command will get you started:

    python three.py

## Assumptions
Cryptography library is installed.

    pip install cryptography

# Problem 3 answer

Padding for "NO PAIN NO GAIN!" is "NO PAIN NO GAIN!\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"

This is because if there is no padding at the end, so no padding to be removed.
A dummy padding block of 16 bytes of hex(16) -> \x10 is added to distinguish between bytes that are padding and bytes that are actually supposed to be there. Bytes that belong may sometimes look like they are padding and this is the work around.
