import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import common

def ctr_counter_fixed_nonce_encrypt(decoded_input_str, key, nonce, counter):
    t1= nonce+str(counter).zfill(8)
    t2= block.openssl_ecb_encrypt(t1, key)
    keystream.append(t2)
    return keystream

if __name__ == "__main__":
    input_str= 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    #input_str= 'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc='
    decoded_input_str= input_str.decode("base64")
    blocklen= 16
    counter= len(decoded_input_str)/blocklen + 1
    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    nonce= '0'*8
    keystream= []

    for i in range(0, counter, 1):
        t3= ctr_counter_fixed_nonce_encrypt(decoded_input_str, key, nonce, i)

    keystream= ''.join(t3)

    encrypted= block.xor(decoded_input_str, keystream)
    decrypted= block.xor(encrypted, keystream)
    print decrypted
