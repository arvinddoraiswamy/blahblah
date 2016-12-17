'''
THIS IS NOT COMPLETE. PUSHING IT TO GIT JUSYT TO BACK THINGS UP.
'''

import hashlib
import sys
import os
import re
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility
import sha1
import block

def pad_message(message):
    '''
    https://tools.ietf.org/html/rfc3174#section-4
    Message Digest(MD) -> SHA1(message). Signature(MD) is verified instead of signature. Much smaller
    '''
    #SHA1 works on a bit string. So converting to binary.
    bin_message= utility.ascii_to_bin(message)
    orig_len_message= len(bin_message)
    if orig_len_message % 512 == 0:
        no_of_sha1_blocks= orig_len_message/512
    else:
        no_of_sha1_blocks= orig_len_message/512 + 1
    total_msg_size= 512 * no_of_sha1_blocks

    #Padding the message as per the RFC with 1 and a bunch of zeros
    bin_message += '1'
    padded_zero_len= total_msg_size - len(bin_message) - 64
    bin_message += '0' * padded_zero_len

    #Guessing all possible lengths
    all_msgs= {}
    for length in range(0, pow(2,16), 1):
        t1= bin_message
        t1+= bin(length)[2:]
        all_msgs[length]= t1

    return all_msgs

def split_into_arrays(orig_signature):
    initializers= [orig_signature[x:x+8] for x in range(0, len(orig_signature), 8)]
    return initializers

if __name__ == "__main__":
    '''
    Alice sends a message to Bob. This message is hashed to verify integrity. The key that is used is prepended to the message which is then hashed (H1) and sent.
    If you choose your message, prepending the previous message to it, the final hash (H2) will have H1 (Previous) as an intermediate state. Eve needs to somehow guess the length of the key so she can pad the original message. This will result in H1 becoming an intermediate state. Once this is done, Eve can add her own text, hash it and append H2 to satisfy the receiver. SHA1 and SHA2 are both vulnerable to this attack. SHA3 is not.
    '''
    message= 'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
    bad_msg= ';admin=true'
    key=   'teddy' 

    #Generate glue padding
    all_msgs= pad_message(message)

    #Get original signature for secret prefix message
    secret_prefix_msg= key+message
    orig_signature= sha1.sha1(secret_prefix_msg, 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)

    #Split original signature into 32 bit words
    t1= split_into_arrays(orig_signature)
    initializers= [int('0x'+x, 16) for x in t1]
    print initializers

    #Calculate spoofed message signature to compare at the end
    spoofed_signature= sha1.sha1(secret_prefix_msg+bad_msg, 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)
    spoofed_signature_1= sha1.sha1(secret_prefix_msg+bad_msg, initializers[0], initializers[1], initializers[2], initializers[3], initializers[4])
    print 'This is what the signature of the message should look like after tampering'
    print spoofed_signature
    print spoofed_signature_1
    print

    #Append bad message to all these messages and compare to spoofed signature
    for key,val in all_msgs.items():
        val += bad_msg
        t1= sha1.sha1(val, initializers[0], initializers[1], initializers[2], initializers[3], initializers[4])
        
        flag= 0
        if t1 == spoofed_signature or t1 == spoofed_signature_1:
            print 'Signature after tampering with the message'
            print 'Length of message', key
            print t1
            print
            flag= 1
            break
        else:
            continue

    if flag == 0:
        print 'Hash match not found. Attack failed\n'
