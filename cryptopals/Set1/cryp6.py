"""
http://crypto.stackexchange.com/questions/8845/finding-a-keylength-in-a-repeating-key-xor-cipher
"""

from __future__ import division
import operator
import sys
import os
import itertools
import re
import base64
import string

def hex_to_ascii(hex_string):
  ascii_string=hex_string.decode("hex")
  return ascii_string

def ascii_to_bin(string):
    hex_string= ascii_to_hex(string) 
    bin_string= hextobin(hex_string)
    return bin_string

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

def hextoint(string):
  hex_str=int(string,16)
  return hex_str

def xor(int1,int2):
  int_xor_result=int1 ^ int2
  return int_xor_result

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

  t2=str(t2)*int(len(hex1)/len(t2))
  if len(hex1) % len(t2) != 0:
    hex2=str(t2)+str(t2)[0:(len(hex1) % len(t2))]
  else:
    hex2=t2

  int1=hextoint(hex1)
  int2=hextoint(hex2)

  int_xor_result=xor(int1,int2)
  if int_xor_result >= 0 and int_xor_result <= 15:
    hex2=str(hex(int_xor_result)[2:]).zfill(2)
  else:
    hex2=str(hex(int_xor_result)[2:])

  if hex2.endswith('L'):
      return hex2[:-1]
  else:
      return hex2

def decode_base64_file(input_file_handle,output_file_handle):
  base64.decode(input_file_handle,output_file_handle)

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

#Get hamming distance for all combinations
def hamming_distance(string1, string2):
    bin_string1= ascii_to_bin(string1)
    bin_string2= ascii_to_bin(string2)

    t1= [i for i in range(min(len(bin_string1), len(bin_string2))) if bin_string1[i] != bin_string2[i]]
    return len(t1) + max(len(bin_string1), len(bin_string2)) - min(len(bin_string1), len(bin_string2))

#Calculate the keys for all the key-lengths and then sort
def calculate_key_length_vignere(buffer):
    MIN_KEYSIZE= 2
    MAX_KEYSIZE= 41
    
    all_hamming_distances= {}
    for keysize in range(MIN_KEYSIZE, MAX_KEYSIZE):
        # We want atleast 6 combinations
        no_of_samples= 6

        # Get all samples
        t2= []
        start= 0
        for c1 in range(0,no_of_samples):
            t1= buffer[start:start+keysize]
            start += keysize 
            t2.append(t1)

        # Get all combinations from the samples
        t3=list(itertools.combinations(t2, 2))

        # Get hamming distances per sample comparison
        s1= []
        s1= [(hamming_distance(value[0], value[1])) for count,value in enumerate(t3)]

        # Calculate average hamming distance per keysize
        all_hamming_distances[keysize]= (sum(s1)/no_of_samples)/keysize

    return all_hamming_distances

#Transpose the buffer, and sort it column-wise
def transpose(buffer, keylen):
    s3= []
    for offset in range(0, keylen):
        s3.append(buffer[offset::keylen])

    return s3

#Try and decrypt KEYLEN worth of text to start off with. If that works, I'll change this to decrypt the whole buffer
def decrypt_buffer(buffer, final_key):
    print 'Inside decrypt buffer'
    s2= []

    for column,val in final_key.items():
        print column,val

    for column,val in final_key.items():
        s2.append(chr(ord(buffer[column]) ^ val))

    print
    print 'Decrypted buffer, first few characters'
    print s2

#Normalize string, mainly to add a penalty for all the non-printable characters
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

#Take each column and XOR it with 0-127. Return a dictionary with all the 128 XOR results
def xor_with_all_ascii(column):
    s1= {}
    for t1 in list(itertools.chain(range(0,128))):
        s2= ''
        for char in list(column):
            s2+= chr(ord(char) ^ t1)

        s1[t1]= s2

    return s1

#Start here
if __name__ == "__main__":
    r1= open('cryp6_input_file','rU')
    f1= open('cryp6_base64_inputfile','w')
    decode_base64_file(r1, f1)
    r1.close()
    f1.close()

    with open('cryp6_base64_inputfile','rU') as f1:
        buffer= f1.read()

    test_string1= 'this is a test'
    test_string2= 'wokka wokka!!!'

    #Checkpoint 1 - Sample string, hamming distance check - WORKS
    test_ham= hamming_distance(test_string1, test_string2)

    if test_ham == 37:
        print "Hamming distance test worked correctly"

        all_hamming_distances= calculate_key_length_vignere(buffer)

        #Tuple that sorts the hamming distances in order and gets just the first 5 entries after sorting - this is just beautiful by Python :)
        s1= sorted(all_hamming_distances.items(), key=operator.itemgetter(1))[:5]

        #Checkpoint 2 - Top 5 keysizes properly sorted in ascending order - WORKS
        for num in range(0,len(s1)-1):
            if s1[num][1] > s1[num+1][1]:
                print 'Hamming distances not properly sorted. Exiting'
                sys.exit(0)

        print "Here are the top 5 smallest keysizes and their corresponding hamming distances"
        print s1
        print
        print "Transposing and solving for each keysize now"
        print '-'*120

        for keylen, value in s1:
            #Flush keys for previous keylength at the start of each iteration else bad things happen ;)
            final_key= {}
            possible_keys= {}

            #Checkpoint 3 - Checking transpose length - WORKS
            transposed_blocks= transpose(buffer,keylen)
            print 'Keylength:',keylen,'Minimum Column size:',len(transposed_blocks[keylen-1]),'Product:',keylen*len(transposed_blocks[keylen-1]),'Buffer len:',len(buffer)
            if keylen*len(transposed_blocks[keylen-1])<= len(buffer):
                print "Trying to get possible keys per column for keylen",keylen

                block_num= 0
                #For each block, XOR the block with ASCII (Decimal 1-127)
                for count,column in enumerate(transposed_blocks):
                    possible_key_chars= []
                    key_chi= {}

                    xor_per_column= xor_with_all_ascii(column)
                    #Checkpoint 4 - Testing XOR code before proceeding - WORKS
                    if column != xor_per_column[0]:
                        print "Something's screwed up in the XOR. Exiting."
                        sys.exit(0)

                    #Do the frequency analysis for each XOR result (0..127) for the column.
                    for k1,v1 in xor_per_column.items():
                        total_chi_square_value= frequencyChiSquare(v1)
                        if total_chi_square_value != -1:
                            key_chi[k1]= total_chi_square_value
                        else:
                            continue
                    '''
                    http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
                    '''
                    #Put the block smallest value first. The key with the smallest chi-square value is the winner.
                    for k1,v1 in sorted(key_chi.items(), key=operator.itemgetter(1)):
                        #print k1,v1
                        possible_key_chars.append(k1)

                    #Assuming that the first key is the correct key :)
                    final_key[block_num]= possible_key_chars[0]
                    block_num += 1

                #Lets try decrypting with any of the keys we've found
                decrypt_buffer(buffer, final_key)
                print '-'*50,'End of block with keylen',keylen,'-'*50
                print

            else:
                print "Something's screwed up while transposing. Exiting."
                sys.exit(0)
    else:
        print "Hamming distance test failed"
        sys.exit(0)
