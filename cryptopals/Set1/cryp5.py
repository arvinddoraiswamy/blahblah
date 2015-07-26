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
  string='Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
  key='ICE'

  encrypted_repetitive_xor_string=utility.xor_repetitive(string,key)
  print encrypted_repetitive_xor_string

main()
