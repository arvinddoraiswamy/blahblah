string='uggc ubfg u4pxz3 ugzy'

import sys
import os

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility

def main():
  rotated_string_array=utility.rotate_string_entire_alphabet(string)

main()
