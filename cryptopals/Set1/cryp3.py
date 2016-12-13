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
    result= utility.check_if_all_ascii(plaintext)
    for k,v in result.items():
        print k,v

main()
