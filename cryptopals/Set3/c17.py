'''
https://blog.skullsecurity.org/2013/padding-oracle-attacks-in-depth#
http://robertheaton.com/2013/07/29/padding-oracle-attack/
'''

import sys
import os
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import common
import random

def pick_random_string_index(length):
    return random.randrange(0,length)

def padding_oracle(encrypted):
    blockcount = len(encrypted)/blocklen
    final= ''

    for enclen in range(len(encrypted),0,-16):
        i2= []
        c2= encrypted[enclen-16:enclen]

        #Message larger than 1 block
        if enclen-16 > 0:
            c1dash= encrypted[enclen-32:enclen-16]
        #Single block message
        elif enclen-16 == 0:
            c1dash= ivsplit

        for bytenum in range(15,-1,-1):
            no_of_pad_chars= blocklen-bytenum
            l1= []
            for middlebyte in reversed(i2):
                t2= middlebyte ^ no_of_pad_chars
                l1.append(hex(t2)[2:].zfill(2).decode("hex"))

            #This is the actual brute-force bit where we guess characters in a specific position
            for i in range(1,256):
                t1= hex(i)[2:].zfill(2).decode("hex")
                c1= '\x41'*bytenum+t1

                #Appending bytes already solved for. This grabs the last byte first, then the second last and so on
                for x in l1:
                    c1= c1+x

                chosen_ct= c1+c2
                decrypted= block.openssl_cbc_decrypt(chosen_ct, key, ivsplit)

                is_padding_correct= block.check_pad(blocklen, decrypted)
                if is_padding_correct == True:
                    #This is for block N-1. Remember. NOT Block N.
                    i2.append(i^no_of_pad_chars)
                    break
                else:
                    continue

        f1= []
        c1dash= c1dash[::-1]
        #CBC here, xor previous block byte by byte (which we solved for) with the target block (which we already have) and get plaintext_per_block
        for i in range(0,16):
            f1.append(chr(ord(c1dash[i]) ^ i2[i]))

        blockcount-= 1
        #Since we have solved stuff in the reverse order, we need to reverse it here to get the plaintext in the right order
        final= ''.join(reversed(f1))+final

    return final

if __name__ == "__main__":
    input_file=   'c17_strings'
    blocklen= 16

    #Get list of strings, base64 decode them and add them to an array
    list_of_strings= []
    t1= common.openfile(input_file)
    for string in t1:
        list_of_strings.append(string.decode('base64'))

    #Pick a random string
    random_index= pick_random_string_index(len(list_of_strings))
    input_str= list_of_strings[random_index]

    #Generate random key to use for all future encryption
    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    
    #Generate a random IV to use in CBC
    iv= '29b28d9f2f56c08a8df1778d7408ba79'
    ivsplit= []
    for count in range(0,len(iv),2):
        ivsplit.append((iv[count]+iv[count+1]).decode("hex"))

    #Pad string & encrypt chosen string with key
    encrypted= block.openssl_cbc_encrypt(input_str, blocklen, key, ivsplit)
    final= padding_oracle(encrypted)
    print final
