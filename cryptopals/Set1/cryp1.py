string='49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

import sys
import os

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility

def main():
  utility.fill_base64_mapping()
  bin_str=utility.hextobin(string)
  base64_str=utility.bintobase64(bin_str)

  print base64_str

main()
