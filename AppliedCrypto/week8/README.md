# Problem 1

Performs cbc padding oracle attack

## Getting Started

For this, you need the rypto.py file in the week8 and one.py in the week8 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one.py


The checker and the sanitizer are both in rypto.py.


## Info

Currently the found strings have additional random bytes added to the end however the data is still there and accurate.
Currently no effort is made to change the iv although this would use the same idea.