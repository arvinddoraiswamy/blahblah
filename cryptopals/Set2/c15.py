import sys
import os
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import utility

if __name__ == "__main__":
    padded_samples= ['ICE ICE BABY\x04\x04\x04\x04','ICE ICE BABY\x05\x05\x05\x05','ICE ICE BABY\x01\x02\x03\x04']
    blocksize= 16

    plaintext= 'ICE ICE BABY'
    padded_plaintext= block.pad_block(plaintext, blocksize)
    for sample in padded_samples:
        print sample
        if sample == padded_plaintext:
            print 'Padding is ok'
        else:
            raise ValueError('Padding is incorrect')
