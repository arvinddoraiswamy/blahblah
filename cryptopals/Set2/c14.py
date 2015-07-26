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
    str= ''
    answer= ''

    #Guess only the last character and go backwards one by one, guessing 1 char at a time. Changing length of random string to be prepended = changing this too :)
    for count in range(146,1,-1):
        encrypted_all_ascii= {}

        #Calculate encryption of 0..n, 0..n-1 and so on
        encrypted_short= block.break_ecb_random_prepend(plaintext[0:count])

        #Set byte to all 256 ASCII characters one at a time and store the encrypted strings in a dictionary 
        for asc in range(0,256):
            t1= plaintext[0:count]+str+chr(asc)
            encrypted_all_ascii[chr(asc)]= block.break_ecb_random_prepend(t1)

        #Compare encrypted stuff with the ASCII dictionary. Where there is a match, you've guessed that character. Changing length (random string) = changing this :)
        for key,value in encrypted_all_ascii.items():
            if value[16:160] == encrypted_short[16:160]:
                str += key
                break
            else:
                continue

    #Join all the characters up
    answer= ''.join(str)
    print answer[:-1]
