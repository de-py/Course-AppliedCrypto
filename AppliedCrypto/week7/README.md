# Problem 1

Performs cbc bit flipping

## Getting Started

For this, you need the rypto.py file in the week7 and one.py in the week7 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one.py


The checker and the sanitizer are both in rypto.py.


## Assumption

That the block value you wish to change is 2 or greater and that you don't try to change an end block.
This is untested because the end block may not be a full block when decrypted and we do not know the length
of the string
