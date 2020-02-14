# hex2Base64 (1a)

This program will convert hex to base64. It does not use any python type conversion functions.


## Getting Started

For this, you only need the hex2Base64.py file in the week1 directory.
Running the following command will get you started:

    python hex2Base64.py


## Assumptions

The biggest assumption is that the string should contain an even number of hex bytes. There is a check for the string being even and the program will not continue otherwise. There is not currently a check to make sure the bytes are only hex digits so the user input is assumed to be hex at the moment.


# b64ConversionTester (1b)

This program compares the functions from hex2Base64.py against pythons built in functions for converting to base64. It will reading in a file of hex strings, run the check, and print true or false if they match.

## Getting Started

For the b64 checker, it is best to have the entire week1 directory. However, assuming you have cloned the repo, you only need to run the command:

    python b64ConversionTester.py hex_strings.txt


## Assumptions

If is important that the hex_strings file only have one hex string per line. You may also replace hex_strings.txt with a file of your own. 

# XOR Function (2)

XORs two hex strings taken from the user

## Getting Started

Assuming you have cloned repo and have week1 folder.. run this command to run through the program:

    python xor_func.py

## Assumptions

Similar assumptions as previous two problems (even number hex, only hex). You should have the week1 directory.

# p3.txt (3)

This does frequency count and proves knowledge and ability to solve the 3rd problem

## Getting Started

    python xor_file.py

## Assumptions

Cloned the repo.. p3.txt is in the same directory as xor_file.py

## Answer:

    ifamanisofferedafactwhichgoesagainsthisinstinctshewillscrutinizeitcloselyandunlesstheevidenceisoverwhelminghewillrefusetobelieveitifontheotherhandheisofferedsomethingwhichaffordsareasonforactinginaccordancetohisinstinctshewillacceptitevenontheslightestevidencetheoriginofmythsisexplainedinthisway
