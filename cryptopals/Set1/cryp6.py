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

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import utility

def decode_base64_file(input_file_handle,output_file_handle):
  base64.decode(input_file_handle,output_file_handle)

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
        s1= [(utility.hamming_distance(value[0], value[1])) for count,value in enumerate(t3)]

        # Calculate average hamming distance per keysize
        all_hamming_distances[keysize]= (sum(s1)/no_of_samples)/keysize

    return all_hamming_distances

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

#Start here
if __name__ == "__main__":
    with open('cryp6_input_file','rU') as f:
        t1= f.read()

    buffer= t1.decode('base64')
    test_string1= 'this is a test'
    test_string2= 'wokka wokka!!!'

    #Checkpoint 1 - Sample string, hamming distance check - WORKS
    test_ham= utility.hamming_distance(test_string1, test_string2)

    if test_ham == 37:
        print "Hamming distance test worked correctly"

        all_hamming_distances= calculate_key_length_vignere(buffer)

        #Tuple that sorts the hamming distances in order and gets just the first N entries after sorting - this is just beautiful by Python :)
        s1= sorted(all_hamming_distances.items(), key=operator.itemgetter(1))[:1]

        #Checkpoint 2 - Top 5 keysizes properly sorted in ascending order - WORKS
        for num in range(0,len(s1)-1):
            if s1[num][1] > s1[num+1][1]:
                print 'Hamming distances not properly sorted. Exiting'
                sys.exit(0)

        print "Here is the smallest keysize and its corresponding hamming distances"
        print s1
        print
        print "Transposing and solving for the keysize now"
        print '-'*120

        for keylen, value in s1:

            transposed_blocks= utility.transpose(buffer,keylen)

            print "Predicted keylength is ",keylen
            #Checkpoint 3 - Checking transpose length - WORKS
            if keylen*len(transposed_blocks[keylen-1])<= len(buffer):
                print "Trying to get keys per column for keylen",keylen
                #For each block, XOR the block with ASCII (Decimal 1-127)
                key= []
                for count,column in enumerate(transposed_blocks):
                    t3= {}
                    xor_per_column= utility.xor_with_all_ascii_string(column)
                    #Checkpoint 4 - Testing XOR code before proceeding - WORKS
                    if column != xor_per_column[0]:
                        print "Something's screwed up in the XOR. Exiting."
                        sys.exit(0)
                    
                    is_ascii= utility.check_if_all_ascii(xor_per_column)
                    pattern= r'[A-Za-z]'
                    regex= re.compile(pattern)
                    for k,v in is_ascii.items():
                        match = regex.findall(v)
                        t3[k]= len(match)

                    #You need the encrypted text where you have the maximum matches, hence you sort the dictionary.
                    x= max(t3, key=t3.get)
                    key.append(x)
                k1= ''.join(key)
                print k1
                final_key= raw_input("Okay. Fix the key displayed above by looking at it manually and enter it to decrypt the text.\n")
                decrypted_hex= utility.xor_repetitive(buffer, final_key)
                decrypted= utility.hex_to_ascii(decrypted_hex)
                print '-'*75
                print decrypted
            else:
                print "Something's screwed up while transposing. Exiting."
                sys.exit(0)
    else:
        print "Hamming distance test failed"
        sys.exit(0)
