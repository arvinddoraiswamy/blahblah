'''
Pad the block so that block % 8 == 0 or block % 16 == 0 depending on block size. The pad character should be the string equivalent of the length of the padding
needed.
'''
import sys
import os

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
if __name__ == "__main__":
    buffer= 'YELLOW SUBMARINE'
    block_size= 20
    padded_buffer= block.pad_block(buffer, block_size)
    print padded_buffer
