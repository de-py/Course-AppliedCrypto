# Problem 1

Conceils encrypted text that has already been decrypted by user and tricks server to decrypt it again for attacker

## Getting Started

For this, you need the rypto.py AND large_prime.py file in the week13 and one.py in the week13 directory.


If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python one.py


## Info and why this works

This works because of homomorphic property. Given plain text a and b, (a^e*b^e) mod n corresponds to encrypted (a*b). Big a value r and multiply with encrypted text c. The new C2 to decrypt equals cr^e mod n. When C2 is decrypted, you simply divide out r and you have plain text.


# Problem 2

Decrypts problem 2

## Getting Started

For this, you need the rypto.py file in the week13 and two.py in the week13 directory.

If you don't have these libraries, pip install them.

    pip install pycrypto
    pip install cryptography

Running the following command will get you started:

    python two.py

## Info
This works because of these websites:
http://diamond.boisestate.edu/~liljanab/ISAS/course_materials/AttacksRSA.pdf #attack 2

https://blog.0daylabs.com/2015/01/17/rsa-common-modulus-attack-extended-euclidean-algorithm/





