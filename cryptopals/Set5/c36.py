import random
import hashlib
import collections
import hmac

def S_saltgen(g, N, P):
    serverdata= collections.namedtuple('serverdata', 'salt v g N P')

    salt= random.randint(0, pow(2,32))
    xH= hashlib.sha256(str(salt) + str(P)).hexdigest()
    x= int(xH, 16)
    v= pow(g, x, N)
    S_saved= serverdata(salt=salt, v=v, g=g, N=N, P=P)
    return S_saved

def C_to_S_first(I,A):
    print 'Server received I and A from the client -', I, A

def S_to_C_first(salt, B):
    print 'Client received salt and B from the server -', salt, B

'''
http://cryptopals.com/sets/5/challenges/36 but mod N for any modexp operations based on https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol#Protocol
If you don't do the modexp % N, the problem takes forever to complete. The modexp does work though, set x to a smaller number and check by doing the math with  
and without mod N
'''
def client_gen_key(salt, P, g, N, B, a, u, k):
    xH= hashlib.sha256(str(salt) + str(P)).hexdigest()
    x= int(xH, 16)

    t1= B - (k * pow(g, x, N))
    t2= a + (u * x)
    S= pow(t1, t2, N)
    K= hashlib.sha256(str(S)).hexdigest()
    print 'Client secret is ', K
    return K

def server_gen_key(A, v, u, b, N):
    t1= A * pow(v, u, N)
    S= pow(t1, b, N)
    K= hashlib.sha256(str(S)).hexdigest()
    print 'Server secret is ', K
    return K

if __name__ == '__main__':
    #Common parameters
    N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2
    k= 3
    I= 'teddy@boo.org'
    P= 'teddybear'

    #Server side salt stuff as a named tuple
    S_saved= S_saltgen(g, N, P)

    #Client to server, first communication
    a= random.getrandbits(256)
    A= pow(g, a, N)
    C_to_S_first(I,A)

    #Server to client, first communication
    b= random.getrandbits(256)
    B= (k * S_saved.v) + pow(g, b, N)
    S_to_C_first(S_saved.salt, B)

    #Generate integer used in math operations to generate a key. Same number is used on both sides
    uH= hashlib.sha256(str(A) + str(B)).hexdigest()
    u = int(uH, 16)

    #Client-side key generation
    cKey= client_gen_key(S_saved.salt, P, g, N, B, a, u, k)

    #Server-side key generation
    sKey= server_gen_key(A, S_saved.v, u, b, N)

    if cKey == sKey:
        print 'Shared key matches'
        secret= 'teddy'
        
        #Calculate client and server HMACs using the client and server keys and compare the 2. If it matches it means SRP is properly implemented
        chmac = hmac.new(cKey, msg=str(S_saved.salt), digestmod=hashlib.sha256).digest()
        shmac = hmac.new(sKey, msg=str(S_saved.salt), digestmod=hashlib.sha256).digest()

        if chmac == shmac:
            print 'OK.'
        else:
            print 'Error computing HMACs'
    else:
        print 'Something is screwed up with the math. Check stuff'
