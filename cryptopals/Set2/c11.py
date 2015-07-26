import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block

if __name__ == "__main__":
    plaintext= 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    is_aes_mode_ecb= block.encryption_oracle(plaintext)
    if is_aes_mode_ecb == 1:
        print "String ",plaintext, "is AES encrypted with ECB mode"
    else:
        print "String ",plaintext, "is AES encrypted with CBC mode"
