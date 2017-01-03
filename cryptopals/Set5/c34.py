import sys
import os
import random
import hashlib
import binascii

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import pki
import block

if __name__ == '__main__':
    #Public numbers used in DH
    p= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2

    print 'This is the normal case'
    #The private random numbers need to be at least 256 bits long keeping the future in mind
    a= random.getrandbits(256)
    A= pow(g, a, p)

    b= random.getrandbits(256)
    B= pow(g, b, p)
    print "B received ", p, g, A
    #User B calculates shared secret and hashes it to get a key. User B also sends B(public) over to A so A can also calculate the shared secret
    s2= pow(A, b, p)

    #User A gets B, calculates shared secret and hashes it to get a key
    print "A received ", B
    s1= pow(B, a, p)
    key= hashlib.sha1(str(s1)).hexdigest()[0:16]
    print "Key used to decrypt is", key

    #Once both sides have created the shared secret, they can use it to encrypt traffic
    msg_to_B= 'Teddy for B'
    msg_to_A= 'Teddy for A'
    block_size= 16

    #This is different for both users
    iv_to_B= '0x29b28d9f2f56c07a8df1778d7408ba79'
    iv_to_A= '0x29c28e9f2556c08a8df1798d7408ba64'

    #A encrypts traffic and sends it to B
    enc_to_B= block.openssl_cbc_encrypt(msg_to_B, block_size, key, binascii.a2b_hex(iv_to_B[2:]))
    print 'Encrypted text from A to B', repr(enc_to_B)

    #B encrypts traffic and sends it to A
    enc_to_A= block.openssl_cbc_encrypt(msg_to_A, block_size, key, binascii.a2b_hex(iv_to_A[2:]))
    print 'Encrypted text from B to A', repr(enc_to_A)
    print '-' * 50

    print 'This is the MITM case'
    #A sends p, g and A to B but it is intercepted by M who sends p, g, p instead. B calculates the shared secret using 'p' instead of A
    s2= pow(p, b, p)

    #B sends back MB to A, but this also is MITMed, dropped and 'p' is sent back to A. Effectively, the attacker has replaced A and B with a value of their own choice #and can hence calculate the shared secret themselves now A now calculates a shared secret using 'p' as well, instead of B
    s1= pow(p, a, p)

    #Both A and B calculate the same key too
    keyA= hashlib.sha1(str(s1)).hexdigest()[0:16]
    keyB= hashlib.sha1(str(s1)).hexdigest()[0:16]
    if keyA == keyB:
        print 'Okay. Keys match. Now both sides use this to encrypt traffic.'
        print "Key used to decrypt is", keyA

    ''' This now means that the only thing that is secret is the private random numbers that User A and User B picked. Since these are never sent over the wire, the MITM attacker does not have it '''
    #A encrypts text, M just passes it on to B
    enc_to_B= block.openssl_cbc_encrypt(msg_to_B, block_size, keyB, binascii.a2b_hex(iv_to_B[2:]))
    print 'Encrypted text from A to B', repr(enc_to_B)

    #B encrypts text, M just passes it on to A
    enc_to_A= block.openssl_cbc_encrypt(msg_to_A, block_size, keyA, binascii.a2b_hex(iv_to_A[2:]))
    print 'Encrypted text from B to A', repr(enc_to_A)

    ''' Generic attack makes sense (http://security.stackexchange.com/questions/91699/why-cant-i-mitm-a-diffie-hellman-key-exchange), but not clear how this parameter injection thing works yet '''
