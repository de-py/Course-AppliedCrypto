#!/usr/bin/env python
import rypto
import sha1
import os




def diffie(p,g):
    a = int((os.urandom(256).encode("hex")),16) % p
    b = int((os.urandom(256).encode("hex")),16) % p
    A = rypto.mod_exp(g,a,p)
    B = rypto.mod_exp(g,b,p)

    s1 = rypto.mod_exp(A,b,p)
    s2 = rypto.mod_exp(B,a,p)

    if s1 == s2:
        print 'Keys are the same'
        return s1

    else:
        print 'Key exchange failed'
        exit()


def main():

    """
    Small session values
    """
    small_ses = diffie(101,53)

    print 'Small session value = ', small_ses
    print 'Small session hash = ', sha1.sha1(str(small_ses))[:32] #truncated to 128 bits

    """
    Big session values
    """

    nist_p = ('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024'
            'e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd'
            '3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec'
            '6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f'
            '24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361'
            'c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552'
            'bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff'
            'fffffffffffff')


    nist_intp =  int(nist_p,16)



    big_ses = diffie(nist_intp, 2)

    print 'Big session value = ', big_ses
    print 'Big session hash = ', sha1.sha1(str(big_ses))[:32] #truncated to 128 bits









if __name__ == "__main__":
    main()

