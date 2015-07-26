'''
Chosen plaintext attack
'''
import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block

if __name__ == "__main__":
    plaintext= 'a' * 1000
    block.break_ecb(plaintext)

    str= ''
    answer= ''
    for count in range(143,0,-1):
        encrypted_all_ascii= {}
        encrypted_short= block.break_ecb(plaintext[0:count])
        for asc in range(0,256):
            t1= plaintext[0:count]+str+chr(asc)
            encrypted_all_ascii[chr(asc)]= block.break_ecb(t1)
        for key,value in encrypted_all_ascii.items():
            if value[0:144] == encrypted_short[0:144]:
                str += key
            else:
                continue

    answer= ''.join(str)
    print answer[:-1]
