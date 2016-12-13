import sys
import os
import re
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block

def process_and_decrypt_string(encrypted_tampered):
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])
    iv= key
    iv_in_binary=  binascii.a2b_hex(iv[2:])

    decrypted= block.openssl_cbc_decrypt(encrypted_tampered, key_in_binary, iv_in_binary)
    if block.exception_high_ascii(decrypted) is not None:
        return 'Text had high ASCII characters', decrypted
    else:
        return 'All clean',None

def process_and_encrypt_string(userdata):
    block_size= 16
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])

    #Setting IV=key to introduce the vulnerability
    iv= key
    iv_in_binary=  binascii.a2b_hex(iv[2:])

    encrypted= block.openssl_cbc_encrypt(userdata, block_size, key_in_binary, iv_in_binary)
    return encrypted

def modify_ciphertext(encrypted):
    t1= [encrypted[x:x+16] for x in range(0, len(encrypted), 16)]
    t1[1]= '\x00' * 16
    t1[2]= t1[0]
    encrypted_tampered= ''.join(t1)
    return encrypted_tampered

def get_key(decrypted):
    t1= [decrypted[x:x+16] for x in range(0, len(decrypted), 16)]
    s1= t1[0]
    s2= t1[2]

    k1= []
    for i in range(0,16):
       k1.append(block.xor(s1[i], s2[i]))
    key= ''.join(k1)

    #This is for sanity checking only. Did we recover the key correctly?
    key_orig=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary_orig= binascii.a2b_hex(key_orig[2:])
    if key == key_in_binary_orig:
        return key
    else:
        return None

if __name__ == "__main__":
    userdata= 'A'*16 + 'B'*16 + 'C'*16
    encrypted= process_and_encrypt_string(userdata)
    encrypted_tampered= modify_ciphertext(encrypted)
    message, decrypted= process_and_decrypt_string(encrypted_tampered)
    print 'Here is the exception thrown when stack traces come back to the user. Never do this.'
    print '-'*75
    print repr(decrypted), message
    print '-'*75
    key= get_key(decrypted)
    if key is not None:
        print 'Key found', repr(key)
    else:
        print 'Key not found. Something wrong in your attack.'
