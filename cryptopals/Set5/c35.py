import sys
import os
import random
import hashlib
import binascii

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block

def dh(g, p):
    #These are then sent over to B who simply Acknowledges that he received g and p
    print 'User B received g and p. Now continue.'

    #Now User A calculates A = g^a mod p and sends it over to User B
    a= random.getrandbits(256)
    A= pow(g, a, p)
    print 'Send A over to User B.'

    #Now User B calculates B = g^b mod p and sends it over to User A
    b= random.getrandbits(256)
    B= pow(g, b, p)
    print 'Send B over to User A.'

    #Shared secret creation - A
    s1= pow(B, a, p)
    keyA= hashlib.sha1(str(s1)).hexdigest()[0:16]
    print 'Shared secret and key for A is', s1, ',', keyA

    #Shared secret creation - B
    s2= pow(A, b, p)
    keyB= hashlib.sha1(str(s2)).hexdigest()[0:16]
    print 'Shared secret and key for B is', s2, ',', keyB

    #Once both sides have created the shared secret, they can use it to encrypt traffic
    msg_to_B= 'Teddy for B'
    msg_to_A= 'Teddy for A'
    block_size= 16


    #A encrypts traffic and sends it to B
    enc_to_B= block.openssl_cbc_encrypt(msg_to_B, block_size, keyA, binascii.a2b_hex(iv_to_B[2:]))
    print 'Encrypted text from A to B', repr(enc_to_B)

    #B encrypts traffic and sends it to A
    enc_to_A= block.openssl_cbc_encrypt(msg_to_A, block_size, keyB, binascii.a2b_hex(iv_to_A[2:]))
    print 'Encrypted text from B to A', repr(enc_to_A)
    print '*' * 50
    return enc_to_A, enc_to_B

'''
The point is that setting the DH group to those specific numbers (1, p, p-1) results in the shared secret always being the same despite choosing random private exponenets a and b, for userA and userB.
'''
if __name__ == '__main__':
    #Public numbers used in DH. User A chooses these to start with
    p= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2
    #This is different for both users
    iv_to_B= '0x29b28d9f2f56c07a8df1778d7408ba79'
    iv_to_A= '0x29c28e9f2556c08a8df1798d7408ba64'

    #Normal case
    print 'This is the normal case'
    dh(g, p)

    #We're now assuming that an attacker can somehow control 'g' on both sides like mentioned here - https://www.reddit.com/r/crypto/comments/4z9xy2/help_with_cryptopals_set_5diffie_hellman/d6u3sen/. #In addition the attacker also MITMs traffic bidirectionally like in the previous challenge
    print 'Attacker MITMs and sets g=1 on both sides'
    g= 1
    enc_to_A, enc_to_B= dh(g, p)
    print 'If g is set to 1, the secret will always be sha1(1)[0:16]'
    keyM= hashlib.sha1('1').hexdigest()[0:16]
    print 'KeyM is', keyM, 'now using it to decrypt traffic'
    dec_to_A= block.openssl_cbc_decrypt(enc_to_A, keyM, binascii.a2b_hex(iv_to_A[2:]))
    dec_to_B= block.openssl_cbc_decrypt(enc_to_B, keyM, binascii.a2b_hex(iv_to_B[2:]))
    print 'Decrypted text for A', dec_to_A
    print 'Decrypted text for B', dec_to_B
    print '-' * 50

    print 'Attacker MITMs and sets g=p on both sides'
    g= p
    enc_to_A, enc_to_B= dh(g, p)
    print 'If g is set to p, the secret will always be sha1(0)[0:16]'
    keyM= hashlib.sha1('0').hexdigest()[0:16]
    print 'KeyM is', keyM, 'now using it to decrypt traffic'
    dec_to_A= block.openssl_cbc_decrypt(enc_to_A, keyM, binascii.a2b_hex(iv_to_A[2:]))
    dec_to_B= block.openssl_cbc_decrypt(enc_to_B, keyM, binascii.a2b_hex(iv_to_B[2:]))
    print 'Decrypted text for A', dec_to_A
    print 'Decrypted text for B', dec_to_B
    print '-' * 50

    print 'Attacker MITMs and sets g=p-1 on both sides'
    g= p-1
    enc_to_A, enc_to_B= dh(g, p)
    print 'If g is set to p-1, the secret will always be sha1(1)[0:16] or sha1(p-1)[0:16]'
    keyM1= hashlib.sha1('1').hexdigest()[0:16]
    keyM2= hashlib.sha1('5772990240153149667393032657087704773338337023325323519225082828').hexdigest()[0:16]
    print 'KeyM is', keyM1, 'now using it to decrypt traffic'
    dec_to_A= block.openssl_cbc_decrypt(enc_to_A, keyM1, binascii.a2b_hex(iv_to_A[2:]))
    dec_to_B= block.openssl_cbc_decrypt(enc_to_B, keyM1, binascii.a2b_hex(iv_to_B[2:]))
    print 'Decrypted text for A', dec_to_A
    print 'Decrypted text for B', dec_to_B
    print '-' * 50
    dec_to_A= block.openssl_cbc_decrypt(enc_to_A, keyM2, binascii.a2b_hex(iv_to_A[2:]))
    dec_to_B= block.openssl_cbc_decrypt(enc_to_B, keyM2, binascii.a2b_hex(iv_to_B[2:]))
    print 'Decrypted text for A', dec_to_A
    print 'Decrypted text for B', dec_to_B
