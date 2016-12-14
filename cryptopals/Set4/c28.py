import sys
import os
import re
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import sha1
import block

message= 'this is a good teddybear'
key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
key_in_binary= binascii.a2b_hex(key[2:])
iv=   '0x41e5efcfb64e362b6e54f7abbecf9503' 
iv_in_binary= binascii.a2b_hex(key[2:])
block_size= 16

#You need the key to create the MAC. So you can't tamper with the message and tag on a new MAC at the end
secret_prefix_msg= key_in_binary + message
encrypted= block.openssl_cbc_encrypt(secret_prefix_msg, block_size, key_in_binary, iv_in_binary)

#This is appended to the message right at the end. The receiver who also has the key will compute the MAC, check if it matches and if not, drop the message
mac= sha1.sha1(secret_prefix_msg)

#This is what an attacker on the wire will see
authenticated_msg= encrypted + '^'*3 + mac

#The attacker then tampers with the message and forwards it over to the receiver
t1= list(authenticated_msg)
t1[3]= 'Z'
tampered_msg= ''.join(t1)

#The receiver then computes the MAC for the tampered message. It doesn't match.
mac_tamp= sha1.sha1(authenticated_msg.split('^'*3)[0])
if mac != mac_tamp:
    print 'Message was tampered. Drop it.'
