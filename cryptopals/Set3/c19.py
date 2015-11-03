import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import common

def ctr_counter_fixed_nonce_encrypt(string, key, nonce, counter):
    t1= nonce+str(counter).zfill(8)
    t2= block.openssl_ecb_encrypt(t1, key)
    return t2

if __name__ == "__main__":
    list_of_strings= common.openfile('c19_strings')
    decoded_str= []
    keystream= []
    blocklen= 16
    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    nonce= '0'*8

    for string in list_of_strings:
        decoded_str.append(string.decode("base64"))

    list_encrypted= []
    for string in decoded_str: 
        t3= []
        keystream= ''
        counter= len(string)/blocklen + 1
        for i in range(0, counter, 1):
            t3.append(ctr_counter_fixed_nonce_encrypt(string, key, nonce, i))
        keystream= ''.join(t3)
        encrypted= block.xor(string, keystream)
        list_encrypted.append(encrypted)

    for enc in list_encrypted:
        print repr(enc)
