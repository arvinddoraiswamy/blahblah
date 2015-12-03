import sys
import os
import re
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block
import common
import utility

if __name__ == "__main__":
    list_of_strings= common.openfile('c20_strings')
    decoded_str= []
    key= '71e6efcfb44e362b6e14f7abbecf5503' 
    nonce= '0'*8

    for string in list_of_strings:
        decoded_str.append(string.decode("base64"))

    #Use the key and a non-random counter to generate a keystream. This keystream is what is used to encrypt stuff eventually.
    list_encrypted= block.ctr_encrypt(decoded_str, key, nonce)

    #Find smallest encrypted string and truncate all other strings to that length
    lengths= {}
    for l1 in list_encrypted:
        lengths[l1]= len(l1)
    keylen= min(lengths.itervalues())

    #53 char length strings in this list here. Join all of them to get 1 large encrypted buffer.
    t2= []
    for l1 in list_encrypted:
        t2.append(l1[0:keylen])
    buffer= ''.join(t2)

    #Transpose the encrypted buffer by grabbing every 53rd character. This creates 53 new strings each of length 60.
    #Each 60 char long string now needs to be solved as if each char was XOR'd with the same character. Coz that's exactly how Vignere actually works.
    #Each column is encrypted with the same key. Repeat this 53 times, as there are 53 strings.
    transposed_blocks= utility.transpose(buffer,keylen)
    k2= []
    for count,column in enumerate(transposed_blocks):
        t3= {}
        xor_per_column= utility.xor_with_all_ascii_string(column)
        is_ascii= utility.check_if_all_ascii(xor_per_column)
        pattern= r'[A-Za-z]'
        regex= re.compile(pattern)
        for k,v in is_ascii.items():
            match = regex.findall(v)
            t3[k]= len(match)

        #You need the encrypted text where you have the maximum matches, hence you sort the dictionary.
        if t3:
            x= max(t3, key=t3.get)
            k2.append(x)
        else:
            k2.append('_')
    k1= ''.join(k2)
    print len(k1), repr(k1)
