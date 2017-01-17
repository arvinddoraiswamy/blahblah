'''
Since the server impersonator does not have 'a' no way they can try and get the password by replaying any client stuff so it has to be something on the server.

Related links:
Attacking v - http://crypto.stackexchange.com/questions/2156/how-realistic-is-a-dictionary-attack-on-a-secure-remote-password-protocol-srp#
'''

import hashlib
import hmac

if __name__ == '__main__':
    N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2
    k= 3
    I= 'teddy@boo.org'
    correctP= 'teddybear'
    salt= '\x00' * 16

    #Server
    Sx= int(hashlib.sha256(salt + correctP).hexdigest(), 16)
    Sv= pow(g, Sx, N)

    #Client
    #a= random.getrandbits(256)
    Ca= 100
    A= pow(g, Ca, N)
    print 'Client sends I and A to the server'

    #Server
    '''
    Send salt, B=kv + g**b % N. This is what is normally done.
    In simplified SRP (this challenge) it is B = g**b % n. So the password is not used by the server while computing B
    '''
    #b= random.getrandbits(256)
    #u= random.getrandbits(128)
    Sb= 200
    B= pow(g, Sb, N)
    u= 63920664291717965292096560917043749486L
    print 'Server sends salt, B and u to the client'

    #Client key generation. Test with incorrect password here.
    clientP= 'teddybear'
    Cx= int(hashlib.sha256(salt + clientP).hexdigest(), 16)
    CS= pow(B, (Ca + (u * Cx)), N)
    CK= hashlib.sha256(str(CS)).hexdigest()
    print 'Client generates a key'

    #Server key generation
    t1= A * pow(Sv, u, N)
    SS= pow(t1, Sb, N)
    SK= hashlib.sha256(str(SS)).hexdigest()
    print 'Server generates a key'

    print 'Comparing keys now'
    if CK == SK:
        print 'Key matches'
    else:
        print 'Something wrong - Passwords do not match'

    chmac = hmac.new(CK, msg=str(salt), digestmod=hashlib.sha256).digest()
    shmac = hmac.new(SK, msg=str(salt), digestmod=hashlib.sha256).digest()
    if chmac == shmac:
        print 'HMACs okay. Nothing was tampered with'
    else:
        print 'HMACs do not match. Maybe you are MITMd'
