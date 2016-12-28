'''
THIS IS NOT COMPLETE. PUSHING IT TO GIT JUSYT TO BACK THINGS UP.
'''

import hashlib
import sys
import os
import re
import binascii
import struct
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility
import slowsha
#import sha1
#import sha1_o
import block

def pad_message(message):
    '''
    https://tools.ietf.org/html/rfc3174#section-4
    Message Digest(MD) -> SHA1(message). Signature(MD) is verified instead of signature. Much smaller
    '''
    #Padding the message as per the RFC with 1 and a bunch of zeros
    message += b'\x80'
    len_message= len(message)
    padded_zero_len= 64 - len_message - 8
    message += b'\x00' * padded_zero_len
    message += struct.pack('>Q', len_message * 8)
    return message

def split_into_arrays(orig_signature):
    initializers= [orig_signature[x:x+8] for x in range(0, len(orig_signature), 8)]
    return initializers

if __name__ == "__main__":
    '''
    Alice sends a message to Bob. This message is hashed to verify integrity. The key that is used is prepended to the message which is then hashed (H1) and sent.
    If you choose your message, prepending the previous message to it, the final hash (H2) will have H1 (Previous) as an intermediate state. Eve needs to somehow guess the length of the key so she can pad the original message. This will result in H1 becoming an intermediate state. Once this is done, Eve can add her own text, hash it and append H2 to satisfy the receiver. SHA1 and SHA2 are both vulnerable to this attack. SHA3 is not.
    '''
    #message= 'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
    message= b'abcde'
    bad_msg= b';admin=true'
    key=   b'teddy' 

    #Get original signature for secret prefix message
    secret_prefix_msg= key+message
    #orig_signature= sha1.sha1(secret_prefix_msg, 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)
    orig_signature= slowsha.sha1(secret_prefix_msg, 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0, None)
    print('Original signature is', orig_signature.hexdigest(), '. Use this to fill up state array')

    #Split original signature into 32 bit words
    #t1= split_into_arrays(orig_signature.hexdigest())
    #initializers= [int('0x'+x, 16) for x in t1]
    initializers= struct.unpack('>5I', orig_signature.digest())
    print('State to reuse in attack is as follows', initializers)

    #Start the actual attack. An attacker is now trying to create a fake message without the key from this point on.

    for keylen in range(0, pow(2,6),1):
        padded_msg= pad_message(key+message) + bad_msg
        forged_msg= padded_msg[keylen:]
        h= slowsha.sha1(bad_msg, initializers[0], initializers[1], initializers[2], initializers[3], initializers[4], len(forged_msg) * 8).digest()
        print(h)
