"""
Write utility functions for all of these in the GUI Tool below - https://blog.malwarebytes.org/intelligence/2013/08/the-malware-archives-pdf-files/
"""
from __future__ import division
import os
import sys
import re
import base64
import binascii
import itertools

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)
import common
import string

base64_alphabet={}

def letter_frequency(string):
  letter_count= {}
  letter_count['e'] = 0
  letter_count['t'] = 0
  letter_count['a'] = 0
  letter_count['o'] = 0
  letter_count['i'] = 0
  letter_count['n'] = 0
  letter_count['s'] = 0
  letter_count['h'] = 0
  letter_count['r'] = 0
  letter_count['d'] = 0
  letter_count['l'] = 0
  letter_count['u'] = 0
  letter_count['c'] = 0
  letter_count['m'] = 0
  letter_count['w'] = 0
  letter_count['f'] = 0
  letter_count['y'] = 0
  letter_count['g'] = 0
  letter_count['p'] = 0
  letter_count['b'] = 0
  letter_count['v'] = 0
  letter_count['k'] = 0
  letter_count['x'] = 0
  letter_count['j'] = 0
  letter_count['q'] = 0
  letter_count['z'] = 0

  split_str= list(string)
  for i in range(0,len(split_str)):
    if split_str[i] == 'e':
      letter_count['e']+=1
    elif split_str[i] == 't':
      letter_count['t']+=1
    elif split_str[i] == 'a':
      letter_count['a']+=1
    elif split_str[i] == 'o':
      letter_count['o']+=1
    elif split_str[i] == 'i':
      letter_count['i']+=1
    elif split_str[i] == 'n':
      letter_count['n']+=1
    elif split_str[i] == 's':
      letter_count['s']+=1
    elif split_str[i] == 'h':
      letter_count['h']+=1
    elif split_str[i] == 'r':
      letter_count['r']+=1
    elif split_str[i] == 'd':
      letter_count['d']+=1
    elif split_str[i] == 'l':
      letter_count['l']+=1
    elif split_str[i] == 'u':
      letter_count['u']+=1
    elif split_str[i] == 'c':
      letter_count['c']+=1
    elif split_str[i] == 'm':
      letter_count['m']+=1
    elif split_str[i] == 'w':
      letter_count['w']+=1
    elif split_str[i] == 'f':
      letter_count['f']+=1
    elif split_str[i] == 'y':
      letter_count['y']+=1
    elif split_str[i] == 'g':
      letter_count['g']+=1
    elif split_str[i] == 'p':
      letter_count['p']+=1
    elif split_str[i] == 'b':
      letter_count['b']+=1
    elif split_str[i] == 'v':
      letter_count['v']+=1
    elif split_str[i] == 'k':
      letter_count['k']+=1
    elif split_str[i] == 'x':
      letter_count['x']+=1
    elif split_str[i] == 'j':
      letter_count['j']+=1
    elif split_str[i] == 'q':
      letter_count['q']+=1
    elif split_str[i] == 'z':
      letter_count['z']+=1

  return letter_count

def normalizeString(str1):
    #This is negative character class...not beginning of string. Anything NOT A-Z won't match this pattern :)
    pattern1= '[^A-Z]'
    penalty= 0

    #Convert string to upper case just so it matches the pattern
    str1= str1.upper()

    #Returns all matches in an array
    non_alphabet= re.findall(pattern1, str1)

    for letter in non_alphabet:
        if letter not in string.printable:
            penalty+=1000
        else:
            continue

    return str1,penalty

#Implement ChiSquare and score all the columns after they are XOR'd
def frequencyChiSquare(column):
    expected_count= {}
    englishLetterFreq = {'E': 12.702, 'T': 9.056, 'A': 8.167, 'O': 7.507, 'I': 6.966, 'N': 6.749, 'S': 6.327, 'H': 6.094, 'R': 5.987, 'D': 4.253, 'L': 4.025, 'C': 2.782, 'U': 2.758, 'M': 2.406, 'W': 2.361, 'F': 2.228, 'G': 2.015, 'Y': 1.974, 'P': 1.929, 'B': 1.492, 'V': 0.978, 'K': 0.772, 'J': 0.153, 'X': 0.150, 'Q': 0.095, 'Z': 0.074}

    #Get the normalized string and the penalty for each non-printable character
    string,penalty= normalizeString(column)

    if len(string) <= 0:
        return -1

    lc= letter_frequency(string)
    expected_count= {key:expected_probability * len(string) for key,expected_probability in englishLetterFreq.items()}

    '''
    http://practicalcryptography.com/cryptanalysis/text-characterisation/chi-squared-statistic/
    '''
    total_chi_square= 0
    for letter,no_of_occurences in lc.items():
        chi_square_per_letter= pow(abs(no_of_occurences - expected_count[letter.upper()]), 2)/expected_count[letter.upper()]
        total_chi_square+= chi_square_per_letter

    #Adding penalty for the non-printable strings that appear in the XOR
    total_chi_square= total_chi_square+penalty
    return total_chi_square

def transpose(buffer, keylen):
    s3= []
    for offset in range(0, keylen):
        s3.append(buffer[offset::keylen])

    return s3

def xor_with_all_ascii_string(string):
    t1= list(string)
    t2= ascii_to_hex(t1)
    hex_string= ''.join(t2)
    s1= xor_with_all_ascii(hex_string)
    return s1

def xor_with_all_ascii(hex_string):
    s2= {}
    s1= [hex_string[i:i+2] for i in range(0,len(hex_string),2)]
    for num in list(itertools.chain(range(0,128))):
        t2=[]
        for x in s1:
            t2.append(chr(int(x,16) ^ num))
            s2[num]= ''.join(t2)
    return s2

def binary_to_ascii(string):
    t2= string[::-1]
    decimal= 0
    for index,value in enumerate(t2):
        if value == '1':
            decimal+= pow(2, index)
        else:
            continue

    return decimal

def fill_base64_mapping():
  alph1=65
  alph2=97
  alph3=48
  alph4=43
  alph5=47

  for i in range(0,26):
    base64_alphabet[i]=chr(alph1)
    alph1+=1

  for i in range(26,52):
    base64_alphabet[i]=chr(alph2)
    alph2+=1

  for i in range(52,62):
    base64_alphabet[i]=chr(alph3)
    alph3+=1

  base64_alphabet[62]=chr(alph4)
  base64_alphabet[63]=chr(alph5)

def hextobin(string):
  bin_str=''
  split_str=list(string)

  for i in split_str:
    temp1=str(bin(int(i,16))[2:].zfill(4))
    bin_str+=temp1

  return bin_str

def split_on_specific_char(string,n):
  split_str=[]
  for i in range(0, len(string), n):
    temp1=string[i:i+n]
    split_str.append(temp1)

  return split_str

def bintobase64(bin_str):
  base64_str=''
  n=6
  for i in range(0, len(bin_str), n):
    temp2=int(str(bin_str[i:i+n]),2)
    base64_str+=str(base64_alphabet[temp2])

  return base64_str

def hextoint(string):
  hex_str=int(string,16)
  return hex_str

def xor(int1,int2):
  int_xor_result=int1 ^ int2
  return int_xor_result

def inttohex(integer):
  hex_xor_result=hex(integer)
  return hex_xor_result

'''
http://www.data-compression.com/english.html
- Case insensitive
- Carriage return converted to space
- Whitelist a-z and space, ignore everything else
'''
def checkEnglishfrequencyCount(string):
  '''
  Testing just this function :)
  '''
  #print repr(string)
  #sys.exit(0)
  letter_count={}
  actual_score= {}
  expected_score= {'a':0.0651738,'b':0.0124248,'c':0.0217339,'d':0.0349835,'e':0.1041442,'f':0.0197881,'g':0.0158610,'h':0.0492888,'i':0.0558094,'j':0.0009033,'k':0.0050529,'l':0.0331490,'m':0.0202124,'n':0.0564513,'o':0.0596302,'p':0.0137645,'q':0.0008606,'r':0.0497563,'s':0.0515760,'t':0.0729357,'u':0.0225134,'v':0.0082903,'w':0.0171272,'x':0.0013692,'y':0.0145984,'z':0.0007836,' ':0.1918182}
  whitelist_pattern= '[a-z ]'

  #Applying normalizing rules as per the page I got the scores from

  #Convert string to lower case
  #print repr(string)
  string= string.lower()

  #Substitute carriage return with space
  string= re.sub('[\r]',' ',string)

  #Remove everything other than lower case a-z and space
  string= re.sub('[^a-z ]','',string)
  #print repr(string)

  letter_count[' '] = 0
  letter_count['e'] = 0
  letter_count['t'] = 0
  letter_count['a'] = 0
  letter_count['o'] = 0
  letter_count['i'] = 0
  letter_count['n'] = 0
  letter_count['s'] = 0
  letter_count['h'] = 0
  letter_count['r'] = 0
  letter_count['d'] = 0
  letter_count['l'] = 0
  letter_count['u'] = 0
  letter_count['c'] = 0
  letter_count['m'] = 0
  letter_count['w'] = 0
  letter_count['f'] = 0
  letter_count['y'] = 0
  letter_count['g'] = 0
  letter_count['p'] = 0
  letter_count['b'] = 0
  letter_count['v'] = 0
  letter_count['k'] = 0
  letter_count['x'] = 0
  letter_count['j'] = 0
  letter_count['q'] = 0
  letter_count['z'] = 0

  split_str= list(string)
  for i in range(0,len(split_str)):
    '''
    Testing specific keys :)
    '''
    if split_str[i] == 'e':
      letter_count['e']+=1
    elif split_str[i] == 't':
      letter_count['t']+=1
    elif split_str[i] == 'a':
      letter_count['a']+=1
    elif split_str[i] == 'o':
      letter_count['o']+=1
    elif split_str[i] == 'i':
      letter_count['i']+=1
    elif split_str[i] == 'n':
      letter_count['n']+=1
    elif split_str[i] == 's':
      letter_count['s']+=1
    elif split_str[i] == 'h':
      letter_count['h']+=1
    elif split_str[i] == 'r':
      letter_count['r']+=1
    elif split_str[i] == 'd':
      letter_count['d']+=1
    elif split_str[i] == 'l':
      letter_count['l']+=1
    elif split_str[i] == 'u':
      letter_count['u']+=1
    elif split_str[i] == 'c':
      letter_count['c']+=1
    elif split_str[i] == 'm':
      letter_count['m']+=1
    elif split_str[i] == 'w':
      letter_count['w']+=1
    elif split_str[i] == 'f':
      letter_count['f']+=1
    elif split_str[i] == 'y':
      letter_count['y']+=1
    elif split_str[i] == 'g':
      letter_count['g']+=1
    elif split_str[i] == 'p':
      letter_count['p']+=1
    elif split_str[i] == 'b':
      letter_count['b']+=1
    elif split_str[i] == 'v':
      letter_count['v']+=1
    elif split_str[i] == 'k':
      letter_count['k']+=1
    elif split_str[i] == 'x':
      letter_count['x']+=1
    elif split_str[i] == 'j':
      letter_count['j']+=1
    elif split_str[i] == 'q':
      letter_count['q']+=1
    elif split_str[i] == 'z':
      letter_count['z']+=1
    elif split_str[i] == ' ':
      letter_count[' ']+=1

  normalized_len_string= len(string)
  #print normalized_len_string
  for letter,no_of_occurences in letter_count.items():
    if no_of_occurences!= 0:
        actual_score[letter]= (no_of_occurences/normalized_len_string)
    else:
        continue

  sum= 0
  error= 0
  for letter,score in actual_score.items():
    sum+=score
    if letter in expected_score.keys():
        error+= abs(expected_score[letter] - score)
        #print 'Letter:',letter,'Expected:',expected_score[letter],'Actual:',score,'Error:', abs(expected_score[letter] - score)
    else:
        continue
  return sum,error

def check_if_all_ascii(plaintext):
  is_ascii={}
  for key in plaintext.keys():
    m1=re.match(r'^[\x09-\x7e]+$', plaintext[key])
    if m1:
      is_ascii[str(chr(key))] = plaintext[key]
  
  return is_ascii

def hex_to_ascii(hex_string):
  ascii_string=hex_string.decode("hex")
  return ascii_string

def ascii_to_hex(string):
  t1=list(string)
  t2=''
  for i in t1:
    t3=re.sub('0x','',str(hex(ord(i))))
    t3=t3.zfill(2)
    t2+=t3

  t2=re.sub('0x','',t2)
  return t2

def xor_repetitive(string,key):
  hex1=ascii_to_hex(string)
  t2=ascii_to_hex(key)

  #print len(string), len(hex1)

  #t2=str(t2)*(len(hex1)/len(t2))
  t2=str(t2)*int(len(hex1)/len(t2))
  #print 'Keylen:',len(t2)
  if len(hex1) % len(t2) != 0:
    hex2=str(t2)+str(t2)[0:(len(hex1) % len(t2))]
  else:
    hex2=t2

  int1=hextoint(hex1)
  int2=hextoint(hex2)

  #print len(hex1),len(hex2)

  int_xor_result=xor(int1,int2)
  if int_xor_result >= 0 and int_xor_result <= 15:
    hex2=str(hex(int_xor_result)[2:]).zfill(2)
  else:
    hex2=str(hex(int_xor_result)[2:])
  #sys.exit(0)

#  hex_xor_result_1=inttohex(int_xor_result)

  if hex2.endswith('L'):
      return hex2[:-1]
  else:
      return hex2

def decode_base64_file(input_file_handle,output_file_handle):
  base64.decode(input_file_handle,output_file_handle)

def base64_to_hex(buffer):
  hex_buffer= binascii.hexlify(buffer)
  return hex_buffer

def get_ecb_blocks(string, ecb_blocksize, are_strings_hex):
  string=re.sub('\n','', string)

  #In hex 2 characters = 1 byte
  if are_strings_hex == 1:
    ecb_blocksize *= 2

  t1= split_on_specific_char(string, ecb_blocksize)
  list_all_16_byte_blocks=""

  for i in t1:
    list_all_16_byte_blocks+= i+'_'

  return list_all_16_byte_blocks

def detect_ecb(blocks):
    max_len_blocks= len(blocks)
    unique_blocks= set(blocks)
    if (len(unique_blocks) != max_len_blocks):
        return 1
    else:
        return 0

def rotate_string_entire_alphabet(string):
  #Alphabet hash. z gets 0 because it's mod 26.
  alphabet={'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':0}

  #Split on every character
  split_str=split_on_specific_char(string,1)

  #Rot 1 to Rot 26
  for j in range(1,26):
    int_rotated_str=[]
    count=0
    #Calculate and store numbers
    for i in split_str:
      if i in alphabet:
        t1=(alphabet[i]+j)%26
        int_rotated_str.append(t1)
        count+=1
      else:
        int_rotated_str.append(i)

    #Get mapped alphabet for the number stored a while ago
    rotated_str=''
    for i in int_rotated_str:
      flag=0
      for key in alphabet.keys():
        if i == alphabet[key]:
          flag=1
          rotated_str=rotated_str+key
      if flag == 0:
        rotated_str=rotated_str+str(i)

    print rotated_str

def ascii_to_bin(string):
    hex_string= ascii_to_hex(string) 
    bin_string= hextobin(hex_string)
    return bin_string

def hamming_distance(string1, string2):
    bin_string1= ascii_to_bin(string1)
    bin_string2= ascii_to_bin(string2)

    t1= [i for i in range(min(len(bin_string1), len(bin_string2))) if bin_string1[i] != bin_string2[i]]
    return len(t1) + max(len(bin_string1), len(bin_string2)) - min(len(bin_string1), len(bin_string2))
