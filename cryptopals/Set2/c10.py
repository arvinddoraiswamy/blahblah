import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import base64

input_file= '10.txt'

if __name__ == "__main__":
    key= 'YELLOW SUBMARINE'
    iv= ((r'\x00') * 16).decode('string-escape')
    block_size= 16

    #This bit actually tests the encryption for cbc code
    #plaintext= 'abcdefghijklmnopqrstuvwxyz'
    #encrypted= block.openssl_cbc_encrypt(plaintext, block_size, key, iv)
    #ciphertext= encrypted

    #This bit solves the actual challenge :)
    with open(input_file) as f:
        t1= f.readlines()

    t2= ''.join(t1)
    ciphertext= base64.b64decode(t2)
    decrypted= block.openssl_cbc_decrypt(ciphertext, key, iv)
    print decrypted
