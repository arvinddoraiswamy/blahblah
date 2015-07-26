'''
Known plaintext attacks
'''

import sys
import os
import re

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility
import common
import block

def main():
    list_of_strings=common.openfile('cryp8_input_file')
    ecb_blocksize= 16
    are_strings_hex= 1
    key= block.generate_random_string(ecb_blocksize)

    #Get 16 byte blocks from every string separated by an _
    l1= [utility.get_ecb_blocks(string, ecb_blocksize, are_strings_hex)[:-1] for string in list_of_strings]
    for count,ciphertext in enumerate(l1, start=1):
        encrypted_blocks= []
        blocks= ciphertext.split('_')

        #Pass the plaintext and encrypted blocks to the detection function, not the raw string
        is_aes_mode_ecb= utility.detect_ecb(blocks)
        if is_aes_mode_ecb == 1:
            print "String %d that is %s is ECB encrypted" % (count, ciphertext.replace("_",""))
        else:
            continue

main()
