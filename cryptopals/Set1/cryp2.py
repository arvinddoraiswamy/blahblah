import sys
import os

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility

string1='1c0111001f010100061a024b53535009181c'
string2='686974207468652062756c6c277320657965'

def main():
  int1=utility.hextoint(string1)
  int2=utility.hextoint(string2)
  int_xor_result=utility.xor(int1,int2)
  hex_xor_result=utility.inttohex(int_xor_result)

  print hex_xor_result[2:-1]

main()
