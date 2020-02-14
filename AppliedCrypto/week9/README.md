# Problem 1 & 2

Performs ctr encryption and decryption

## Getting Started

For this, you need the rypto.py file in the week9 and one-two.py in the week9 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one-two.py


The checker and the sanitizer are both in rypto.py.


## Info

Hopefully does everything but a file with more than 256 blocks.


# Problem 3

Performs ctr bit flipping. Checks to see if ';admin=true;' exists anywhere in decrypted value

## Getting Started

For this, you need the rypto.py file in the week9 and three.py in the week9 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python three.py


The checker and the sanitizer are both in rypto.py.


## Info

Well you specify a block you want changed and assuming the block you pick exists, it inputs my admin block and then checks. You can change the user data to wherever. Of the decrypted original value block, you can input the new block in user_data area or pre-pended and appended area, I think.
