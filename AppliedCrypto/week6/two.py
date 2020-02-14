#!/usr/bin/env python
import rypto



#Example \x02 as last byte should be \x03\x03\x03 and not \x03\x03\x01
def same_byte_check(hx,num_bytes):

    if len(set(hx[-num_bytes:])) == 1: #If last bytes in list are all the same
        pass
    else:
        raise ValueError('The padding bytes are not all the same')

#Checks against default padding function. Helpful to confirm block_size check
def block_size_check(b_string, block_size):
    try:
        rypto.unpad(b_string,block_size)

    except Exception:
        raise ValueError('The padding bytes do not match the block size')

def is_padding(the_string, block_size):
    hx = the_string.encode("hex")
    hx = rypto.split(hx,2)
    last = hx[-1] #Last byte in string
    num_bytes = int(last,16)

    if num_bytes == 1:
        block_size_check(the_string,block_size) #Checks to make sure valid to block size
        print 'Assuming it is ACTUALLY only padded with one byte:' #If it made it past block size check
        return rypto.unpad(the_string,block_size)

    else:
        try:
            same_byte_check(hx,num_bytes) #Checks for ending in correct number of bytes and the same byte
            block_size_check(the_string,block_size)#Checks again blocksize with default padding function
            return rypto.unpad(the_string,block_size)#Returns block size with assumption it made it this far without errors
        except ValueError as e:
            raise


#Main Function
if __name__ == "__main__":

    try_string = 'This is a Saturday\x03\x02\x01'
    print is_padding(try_string, 160)