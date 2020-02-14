#!/usr/bin/env python
import time

#Convert binary to hex using a dictionary
def hex_dict(key):
    hex_dict = {'0000': '0',
                '0001': '1',
                '0010': '2',
                '0011': '3',
                '0100': '4',
                '0101': '5',
                '0110': '6',
                '0111': '7',
                '1000': '8',
                '1001': '9',
                '1010': 'A',
                '1011': 'B',
                '1100': 'C',
                '1101': 'D',
                '1110': 'E',
                '1111': 'F',
                }
    return hex_dict[key]
#Converts hex digit into corresponding 4 bits
def bin_dict(key):
    bin_dict = {'0':'0000',
                '1':'0001',
                '2':'0010',
                '3':'0011',
                '4':'0100',
                '5':'0101',
                '6':'0110',
                '7':'0111',
                '8':'1000',
                '9':'1001',
                'A':'1010',
                'B':'1011',
                'C':'1100',
                'D':'1101',
                'E':'1110',
                'F':'1111',
                }
    return bin_dict[key]

#Converts index of 6 bits and returns correct value from X, pre-defined by Base64 index table
#Obviously, keeps the '=' sign if present
def base_64(key):
    if key == "=":
        return "="
    
    elif key == "==":
        return "=="
    else:
        x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        return x[key]

#Converts lower case to upper case, otherwise, stay the same
def upper_case(key):
    alphabet = dict(a = 'A', b = 'B', c = 'C', d = 'D',
                    e = 'E', f ='F')

    if key in alphabet.keys():
        return alphabet[key]
    else:
        return key

#Converts string of binary to the proper hex value
def make_hex(value):
    l = split_stuff(value,4)
    g = ''
    for i in l:
        g += hex_dict(i)
    return g


#Splits a string into a list of n characters per element. e.g. "abcdef" --> ["ab", "cd", "ef"] 
def split_stuff(hex_string,n):
    l = []
    for i in range(0,len(hex_string),n):
        l.append(hex_string[i:i+n])
    return l

#Converts a string from lower case to upper case if not already
def make_upper(hex_string):
    x = ''
    for i in hex_string:
        x += upper_case(i)
    return x

#Makes a string binary, no addition of bytes
def make_bin_2(hex_string):
    x = ''
    for i in hex_string:
        x += bin_dict(i)

    return x

#Makes a string binary and for purpose of base64, adds bytes where needed
def make_bin(hex_string):
    x = ''
    if len(split_stuff(hex_string,2)) % 3 == 0:
        pass
    
    if len(split_stuff(hex_string,2)) % 3 == 1:
        hex_string += '0000'

    
    if len(split_stuff(hex_string,2)) % 3 == 2:
        hex_string += '00'
    
    for i in hex_string:
        x += bin_dict(i)

    return x

#Converts the binary to decimal the old fashioned way
def bin_decimal(val):
    dec = 0
    for i in range(0,len(val)):
        dec += (2**i)*int(val[::-1][i])
        
    return dec

#Converts 6 bits to corresponding decimal value and adds them to a list
#Exceptions made for purpose of base64
def dec_list(binary):
    l1 = []
    l2 = []
    if binary[-12:] == '000000000000':
        l2.append("==")
        binary = binary[0:-12]
    elif binary[-6:] == '000000':
        l2.append("=")
        binary = binary[0:-6]

    for i in split_stuff(binary,6):
        l1.append(bin_decimal(i))

    return l1+l2

#Checks to see if string is even number of values
def is_even(hex_string):
    if len(hex_string) % 2 == 0:
        return True
    else:
        return False
#Converts the list of decimal values to base64 using the base64 index function
def finish_it(dec):
    l = ''
    for i in dec:
        l += base_64(i)
    return l

#Makes every case a uniform string
#Had some help from -->
#http://stackoverflow.com/questions/8139746/implement-python-replace-function-without-using-regexp
def replace(s,value,change):
    for i in xrange(len(s)):     
        if s[i:i+len(value)] == value:
            s = s[:i] + change + s[i+len(value):]
        
    return s

def standardize(hex_s):
    hex_s = replace(hex_s,' ','')
    hex_s = replace(hex_s,'0x', '')
    if is_even(hex_s):
        return hex_s
    else:
        print "Enter an even lengthed string next time."
        time.sleep(1)
        print "Exiting.."
        time.sleep(1)
        exit()

#Does everything
def hex2b64(hex_s):
    hex_s = standardize(hex_s)
    upper_hex = make_upper(hex_s)
    binary = make_bin(upper_hex)
    dec =  dec_list(binary)
    return finish_it(dec)

if __name__ == '__main__':
    hex_string = raw_input("Enter hex string: ")
    answer = None
    answer = hex2b64(hex_string)

    print "User input: \n" + hex_string
    print "User input to base_64: \n" + answer
