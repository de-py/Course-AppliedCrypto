#!/usr/bin/env python
import rypto
import sys
import large_prime


def solve(s0,s1,s2,m):
    c0 = s0.enc(m)
    c1 = s1.enc(m)
    c2 = s1.enc(m)


    ms0 = s1.n * s2.n
    ms1 = s0.n * s2.n
    ms2 = s0.n * s1.n
    N012 = s0.n * s1.n * s2.n


    one = (c0 * ms0 * rypto.mulinv(ms0,s0.n))
    two = (c1 * ms1 * rypto.mulinv(ms1,s1.n))
    three = (c2 * ms2 * rypto.mulinv(ms2,s2.n))

    c = (one + two + three) % N012

    return c

def main():
    e = 3

    print 'Setting up server 1'
    s0 = rypto.rsa(e)

    print 'Setting up server 2'
    s1 = rypto.rsa(e)
    print 'Setting up server 3'
    s2 = rypto.rsa(e)



    m = 'Trying a different message'

    c = solve(s0,s1,s2,m)

    cubed = int(round(c ** (1. / 3)))

    hexad = rypto.standard(hex(cubed))
    print hexad.decode("hex")



if __name__ == "__main__":
    main()