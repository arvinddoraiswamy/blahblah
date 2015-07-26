import sys
import os
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import utility

def profile_for(email):
    chars_to_filter=['&','=']
    email= block.eat_chars(email, chars_to_filter)
    profile= 'email='+email+'&uid=10&role=user'
    return profile

if __name__ == "__main__":
    email= 'foo@googleadmin'+'\x11'*11+'.in'
    profile= profile_for(email)

    length= 16
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    profile= block.pad_block(profile, length)
    encrypted= block.openssl_ecb_encrypt(profile, key[2:])
    fuzz=   encrypted[0:16]+encrypted[32:48]+encrypted[16:32]
    decrypted= block.openssl_ecb_decrypt(fuzz, key[2:])
    print decrypted
