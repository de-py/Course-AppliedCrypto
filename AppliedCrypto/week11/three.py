#!/usr/bin/env python
import rypto
import sha1
import os


def setup():
    nist_p = ('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024'
            'e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd'
            '3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec'
            '6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f'
            '24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361'
            'c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552'
            'bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff'
            'fffffffffffff')

    n =  int(nist_p,16)
    g = 2
    k = 3
    i = 'Bob'
    p = 'verygoodpassword'

    initial = rypto.srp(n,g,k,i,p) #Values listed tecnically "shared"
    return initial



def main():

    session = setup() #Setup mutual variables
    a = int((os.urandom(256).encode("hex")),16) % session.n #Secret value A (For client)
    A = rypto.mod_exp(session.g,a,session.n)
    i = session.i #username (will soon send)
    #client_recv = None

    """
    Server stores the password using the steps:
    1. Generate salt as a random integer
    2. Generate string xH = SHA256(salt|password)
    3. Convert xH to integer x
    4. Generate v = g^x mod N
    5. Save everything but x, xH
    """
    session.store() #Simulating server storing values to db


    """
    Client -> Server:
    """
    #session.client_send(i, A) #Simulating sending username and public A for auth
    session.client_send(i, 0) #Hacker sends 1

    """
    Server -> Client:
    """
    user_recv = session.response() #Simulating receiving salt and public B from server
    client_recv = {'s': user_recv[0], 'B':user_recv[1] } #Storing previous line into something easier to understand


    """
    Server, Client:
    """

    session.calc_u() #Server calculating u


    """
    Server:
    1. Generate S = (A*v^u)^b mod N
    2. Generate K = SHA256(S)
    """
    session.generate_k()

    """
    Validate
    """
    print 'Hacker trying Key 0....'
    hacker_k = rypto.sha256(str(0))
    user_try = rypto.sha256(hacker_k+str((client_recv['s'])))
    session.validate(user_try)







if __name__ == "__main__":
    main()

