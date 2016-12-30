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

def send_to_public_B(p, g, A):
    b= random.getrandbits(256)
    B= pow(g, b, p)
    print "B received ", p, g, A

    #B calculates shared secret and hashes it to get a key
    s2= calc_shared_secret(A, b, p)
    return B

def calc_shared_secret(public, private, modulus):
    secret= pow(public, private, modulus)
    return secret

if __name__ == '__main__':
    #Public numbers used in DH
    p= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2

    #The private random numbers need to be at least 256 bits long keeping the future in mind
    a= random.getrandbits(256)
    A= pow(g, a, p)
    B= send_to_public_B(p, g, A)

    #A gets B, calculates shared secret and hashes it to get a key
    print "A received ", B
    s1= calc_shared_secret(B, a, p)
    key= hashlib.sha1(str(s1)).hexdigest()[0:16]

    msg_to_B= 'Teddy for B'
    msg_to_A= 'Teddy for A'
    block_size= 16
    iv_to_B= '0x29b28d9f2f56c07a8df1778d7408ba79'
    iv_to_A= '0x29c28e9f2556c08a8df1798d7408ba64'

    enc_to_B= block.openssl_cbc_encrypt(msg_to_B, block_size, key, binascii.a2b_hex(iv_to_B[2:]))
    enc_to_A= block.openssl_cbc_encrypt(msg_to_A, block_size, key, binascii.a2b_hex(iv_to_A[2:]))
    print 'Encrypted text from A to B', repr(enc_to_B)
    print 'Encrypted text from B to A', repr(enc_to_A)
