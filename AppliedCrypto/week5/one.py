#!/usr/bin/env python
import rypto


def size_detect(response, original_len,user_input):
    for i in range(2,51):
        new_ui = i * user_input # 'XX', add one each time
        response = oracle.encrypt(new_ui) #New response from oracle
        new_len = len(response) #New length of response

        if new_len != original_len: #If length is not the same, calc. the jump
            return new_len-original_len



    print 'Did not detect size. Should not continue.'

    exit() #Not found





def ascii_cycle(cblock1,cblock2):
    cookie = ''
    for i in range(0,256): #Ascii values 0-255
        try_string = cblock1 + chr(i) + cblock2 #Block combo formula
        hx_try = try_string.encode("hex") #Convert to hex to encrypt (required)
        encrypted = oracle.encrypt(hx_try) #Returns ascii
        if rypto.ecb_detect(encrypted): #If its detected (If 1)
            cookie += chr(i) #Add to selected

        return cookie

#Main Function
if __name__ == "__main__":

    file_name = "Cookie64.txt" #Name of file, added to this file for convenience

    oracle = rypto.ecb_cookie_oracle(file_name)

    #A
    user_input = 'A'.encode("hex")
    print 'A.\nDetecting key size..'
    Aresponse = oracle.encrypt(user_input) #Response from oracle
    original = len(Aresponse) #Original length of response with a single x

    answer = size_detect(Aresponse,original,user_input)
    print 'Key size detected:', answer
    print 'Moving on..'


    #B
    Bresponse = oracle.encrypt(user_input*answer*2) #Encrypt "A" * 32
    print 'B.\nDetecting encryption mode..'
    detected = rypto.ecb_detect(Bresponse)
    if detected:
        print "ECB detected.\nMoving on.."
    else:
        print "ECB not detected. Not sure how to proceed."
        print "Exiting."
        exit()


    #C
    print 'C.\nBreaking ecb encryption cookie..'
    block = ''
    full_string = ''



    """
    This is somewhat like a counter. Assumes string is somewhat short.
    """
    for h in range(1,50):

        """
        This creates two bocks and uses for loop to remove a's from blocks
        """
        for i in range(1,answer+1):
            cblock1 = "A" * (answer-i) + full_string + block #First block grows each time
            cblock2 = "A" * (answer-i) #Second block just gets smaller


            """
            This cycles through ascii
            """
            for j in range(0,256):
                try_string = cblock1 + chr(j) + cblock2 #Block combo formula
                hx_try = try_string.encode("hex") #Convert to hex to encrypt (required)
                encrypted = oracle.encrypt(hx_try) #Returns ascii

                """
                This detects ECB. h --> 16*h. Bigger blocks - 32, 48, etc.
                """
                if rypto.ecb_detect_n(encrypted,h): #If its detected (If 1)
                    block += chr(j) #Add to selected
                    break

        full_string += block
        block = ''

    print 'Cookie found:\n',full_string








