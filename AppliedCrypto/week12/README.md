# Problem 1

Encrypts and Decrypts RSA

## Getting Started

For this, you need the rypto.py AND large_prime.py file in the week12 and one.py in the week12 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one.py


## Info

Not planning to "roll my own" method to encrypt strings longer than modulus.. as per this stackexchange answer (http://stackoverflow.com/questions/5866129/rsa-encryption-problem-size-of-payload-data) and lack of certainty on the approach.

Also, code in problem 1 is ported to classes for problem 2 only. Same functions though.


# Problem 2

This program breaks RSA with a low prime. Currently only partial message is discovered.

## Getting Started

For this, you need the rypto.py file in the week12 and two.py in the week12 directory.

If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python two.py

## Info

Message must be larger than a few values or it will not decrypt correctly to print. Not sure why. Obviously it can't be too big either.





