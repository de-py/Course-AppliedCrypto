# Problem 1

Diffie-hellman

## Getting Started

For this, you need the rypto.py AND sha1.py file in the week11 and one.py in the week11 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one.py


## Info

Uncertain what the hasing key was supposed to be because sha1 is more than 128 bits. So this was chopped accordingly


# Problem 2

This program implements srp

## Getting Started

For this, you need the rypto.py file in the week11 and two.py in the week11 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python two.py



## Info
Does a sudo back and forth between client and server


# Problem 3

This program show how to break srp

## Getting Started

For this, you need the rypto.py file in the week11 and three.py in the week11 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python three.py


## Info
Basically hacker gets what is minimal from the server and responds with a fake key.

#Problem 3 answer..
The server must be sure to check if the public A sent from the client is equal to 0.
This will cause all future calculations to be predictable by the potential attack.