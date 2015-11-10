import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import common

if __name__ == "__main__":
    list_of_strings= common.openfile('c20_strings')
    decoded_str= []
    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    nonce= '0'*8

    for string in list_of_strings:
        decoded_str.append(string.decode("base64"))

    #Use the key and a non-random counter to generate a keystream. This keystream is what is used to encrypt stuff eventually.
    list_encrypted= block.ctr_encrypt(decoded_str, key, nonce)
