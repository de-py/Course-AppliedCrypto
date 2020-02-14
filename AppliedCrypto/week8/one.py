#!/usr/bin/env python
import rypto


def single_block(enc,level):
    split_up = rypto.split(enc,16) #Split up values into blocks
    x = range(0,16) #0,1,2,3,4,5,6,7,...
    y = x[::-1] #X backwards (16,15,14,...)

    full = [] #Will hold "pre" values

    maintain = '' #Will maintain decrypted values


    for c,(i,j) in enumerate(zip(x,y)):
        goal = i+1
        extra = ''

        for z in full[::-1]: #Values stored when combination was correct.
            extra += chr(z^goal)

        k1 = split_up[level][j] #Single value trying to crack
        k2 = split_up[level][:j] #String up to the single value trying to crack

        for h in [chr(i) for i in range(0,256)]: #For h in list of every ascii value
            pre = ord(k1)^ord(h) #Xor with guessed letter and current encrypted value, before XOR with goal padding

            final = pre^goal #XOR with goal padding

            split_up[level] = k2 + chr(final) + extra #Combine (Part up to guess) (Guess^hexpadd) (Previous guesses^newpadding)
            split_up = split_up[:level+2]


            joined = ''.join(split_up) #Combine list into one string

            try:
                response = webapp.decrypt(joined)

            except ValueError as e:
                pass

            if response[0]: #If True

                if goal == ord(h) == 1:
                    continue
                else:
                    maintain += h
                    full.append(pre) #Store the two values, letter and encrypted letter xored.
                    break

            else:
                #print response[1].encode("hex")
                pass

        #print maintain.encode("hex")

        #else: #Occurs if for loop broke
        #    print 'nope'
        #    break
        #print 'maintain',maintain[::-1]


    return maintain[::-1] #Backwards


def num_of_blocks(mess):
    value = len(mess)/16
    rem = len(mess) % 16

    blocks = None

    """
    If there is a remainder, add an extra block
    """
    if rem == 0:
        blocks = value

    else:
        blocks = value+1

    return blocks


if __name__ == "__main__":
    message = open("w8.txt").readlines()
    for l,q in enumerate(message):
        sentence = ''
        q = q.decode("base64")
        webapp = rypto.webapp() #encryption class (oracle)
        enc = webapp.encrypt(q) #encrypted value

        num_blocks = num_of_blocks(enc)

        for m in range(0,num_blocks): #For every block (after 0)
            try:
                sentence += single_block(enc,m) #Check for one block
            except ValueError as e:
                print "I guess were skipping this one"

        print 'Message', l
        try:
            print rypto.unpad(sentence,128)
        except ValueError as e:
            print sentence




