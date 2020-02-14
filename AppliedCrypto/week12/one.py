#!/usr/bin/env python
import rypto
import sys
import large_prime
sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)



#Wikipedia
# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


#Wikipedia
# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def euler(p,q):
    return (p-1)*(q-1)


def find_p_q():
    p = None
    q = None
    while(1):
        print 'Trying to find p..'
        p = large_prime.generateLargePrime(2048)
        if isinstance(p,str):
            pass
        else:
            print 'p found.'
            break;
    while(1):
        print 'Trying to find q..'
        q = large_prime.generateLargePrime(2048)
        if isinstance(q,str):
            pass
        else:
            print 'q found'
            break;
    return p,q



def main():
    p,q = find_p_q() #1
    print 'Moving on..'

    n = p*q # 2

    et = euler(p,q) # 3

    e = (2**16)+1 # 4

    d = mulinv(e,et) #5

    #6 NA

    """
    Test values
    """
    m1 = 8049
    encm1 = rypto.mod_exp(m1,e,n)
    decm1 = rypto.mod_exp(encm1,d,n)

    print 'Checking m1 is decrypted correctly'
    print m1,decm1,m1 == decm1

    m2 = 'Hi this is short'
    m2encoded = int(m2.encode("hex"),16)
    encm2 = rypto.mod_exp(m2encoded,e,n)
    decm2 = rypto.mod_exp(encm2,d,n)
    hexad = rypto.standard(hex(decm2))
    decm2b = hexad[:-1].decode("hex")
    print 'Checking m2 is decrypted correctly'
    print m2,decm2b,m2 == decm2b




if __name__ == "__main__":
    main()

