# Problem 1

This program will encrypt (xor) an acsii string with an ascii key


## Getting Started

For this, you only need the rypto.py file in the week2 and one.py in the week2 directory.

Running the following command will get you started:

    python one.py


## Assumptions
You have directory cloned, your input is in ascii (not hex)


# Problem 2

This will guess the length of the key of a base64 encoded string that was xor'd.
After guessing the length of the key, it will try to guess the key itself by xoring chunks of data with a space (' ')


## Getting Started

For this, you need the base64 file (p2.txt), two.py, and rypto.py

    python two.py (filename)


## Assumptions

You have the directory cloned. It will only xor with ' ', not say the character 'e'.


# Questions and Answers

**What is the encryption key?**<br>
iceiceiceiceiceiceiceiceiceiceiceiceiceiceice

**How long is it?**<br>
45 characters


**Is it really as long as your algorithm
determined?**<br>
No

**If not, then what is the actual key and its length?**<br>
ice --> 3 characters

**Why do you think there is a difference?**<br>
The key length is a multiple of the guessed key length
