import sys
import os
import re

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility
import common

def main():
  count=0
  list_of_strings=common.openfile('cryp4_input_file')
  for string in list_of_strings:
    count+=1
    string=re.sub('\n','',string)

    plaintext=utility.xor_with_all_ascii(string)
    is_ascii=utility.check_if_all_ascii(plaintext)

    print '\n============ '+str(count)+' ---- '+string+' ===========\n'
    for key in is_ascii.keys():
      print key+' ----- '+is_ascii[key]

main()
