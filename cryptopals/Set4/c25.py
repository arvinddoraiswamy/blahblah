#Adding directory to the path where Python searches for modules
import os
import sys
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import common
import block

'''
- Edit the ciphertext using key, nonce, counter, offset and newtext
- Now think of an attacker who has ciphertext, can choose offset and newtext but NOT the key, nonce or counter. This attacker must be able to recover plaintext

Questions:
- What does "but hold on to it" mean for the random key I am not supposed to know?
    - Internally the program should use the key for decryption, but attacker doesn't have this

- Should I be using random nonces during encryption or does it not matter, since attacker won't have it anyway.
    - Doesn't matter

- If nonces are random per block, isn't that the correct way to implement CTR? Why is this breakable?
    - nonces are generated per-message, not per-block. if you generate them per block you have to transmit a list of nonces that's as long as your original message
'''

if __name__ == "__main__":
    filename= '25.txt'
    content= common.openfile(filename)

    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    nonce = '0'*8
    enc_string= block.ctr_encrypt_string(''.join(content), key, nonce)

    plaintext= ''
    for offset in range(0, len(enc_string)):
        for guess in range(0,127):
            t1= block.decrypt_ctr_byte(enc_string[offset], offset, chr(guess))
            if t1 is not None:
                plaintext += chr(guess)
                break
            else:
                continue
    print plaintext
        
