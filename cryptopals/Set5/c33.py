import random
import hashlib

def dh_calc(g, a, b, p):
    ''' Use the 3 argument form of pow() for large numbers if you also need a modulus '''
    A= pow(g, a, p)
    B= pow(g, b, p)

    #This is the shared secret
    s1= pow(A, b, p)
    s2= pow(B, a, p)

    if s1 == s2:
        print "Shared secret is ", s1
    else:
        print "You did something wrong with the math"

    key= hashlib.sha256(str(s1)).hexdigest()
    print "Derived key is 32 bytes of data", key

if __name__ == '__main__':
    #Public numbers used in DH
    p= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2

    #The private random numbers need to be at least 256 bits long keeping the future in mind
    a= random.getrandbits(256)
    b= random.getrandbits(256)
    dh_calc(g, a, b, p)
