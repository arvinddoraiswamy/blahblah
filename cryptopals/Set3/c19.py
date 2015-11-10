'''
37
0
37
He, too, has been changed in his turn
'''

import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import common

def guess(list_encrypted):
    string_index= int(raw_input("Which string do you want to guess from?"))
    string= list_encrypted[string_index]

    start_offset= int(raw_input("Enter start offset of guess:"))
    end_offset  = int(raw_input("Enter end offset of guess:"))
    enc= string[start_offset:end_offset]
    guess_len= end_offset-start_offset

    dec         =     raw_input("Guessed plain text:")

    #Check so you enter the right number of characters while you actually guess stuff and not head scratch where you're going wrong :)
    if len(dec) != guess_len:
        print "Guess length incorrect.Exiting"
        print
        sys.exit(0)

    #CT xor PT = key based on stream cipher property. Get the key for one string and re-use the key to try and decrypt the rest of the encrypted strings.
    key= block.xor(enc, dec)
    t4= []
    for count,s1 in enumerate(list_encrypted):
        t3= s1[start_offset:end_offset]
        t4.append(block.xor(key[0:len(t3)],t3))

    return t4

if __name__ == "__main__":
    list_of_strings= common.openfile('c19_strings')
    decoded_str= []
    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    nonce= '0'*8

    for string in list_of_strings:
        decoded_str.append(string.decode("base64"))

    #Use the key and a non-random counter to generate a keystream. This keystream is what is used to encrypt stuff eventually.
    list_encrypted= block.ctr_encrypt(decoded_str, key, nonce)

    #Guess stuff manually bit by bit, based on common letters that lines might start with
    dec= guess(list_encrypted)
    for count,string in enumerate(dec):
        print count, string
