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

