# Problem 1

This program will decrypt w4p1.txt, the base64 encoded file of aes-cbc encryption, given a key and iv.


## Getting Started

For this, you need the rypto.py file in the week4 and one.py in the week4 directory.
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


##### About replacing the key

Please make the key a string of hex characters without additional characters.
At most, it could accept 0x and also spaces, but nothing much fancier than this.

End result after rypto.standardize will be of type string containing hex digits. e.g. 'ffee21'

Due to the standardize function, your key, (#AESKeyToChange), COULD potentially look like this:<br>
'0xff 0xee 0x21'<br>
'ff ee 21'<br>
'0xff 0xee 0x21'<br>

And it probably shouldn't contain /'s of any kind.

# Problem 2

This program will generate keys, append bytes, prepend bytes, generate ivs,
properly pad for aes, and detect whether ecb or cbc mode was used. Basically
it should be everything asked of problem 2.

## Getting started

Same as problem 1.

  python two.py

## Assumption

The keys must be the same format, type, as when generated with os.urandom.

# Answer (Updated after deadline)

It might not be able to detect all ecb occurrences if there aren't any repeating blocks.
