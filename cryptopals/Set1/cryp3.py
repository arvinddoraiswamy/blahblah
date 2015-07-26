import sys
import os

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility

string1='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

def main():
    plaintext=utility.xor_with_all_ascii(string1)

    for xor_char,line in plaintext.items():
        letter_count, score, other_count= utility.checkEnglishfrequencyCount(line)

        if other_count == 0:
            print line, score, other_count
        else:
            continue

    '''
    is_ascii=utility.check_if_all_ascii(plaintext)

    for key in is_ascii.keys():
        print key+' ----- '+is_ascii[key]
    '''

main()
