'''
message1 = "Hello World"
message2 = "the program"
message3 = "a cool days"
'''

import sys

#inputfile= 'testinput'
inputfile= 'c100'
def get_ciphertexts(inputfile):
    with open(inputfile,'r') as f:
        t1= f.readlines()

    ct= [i.rstrip("\n") for i in t1]
    return ct

def xor_ciphertexts(ct, current_ct_target_num):
    xored_cts= {}
    '''
    XOR Target CT with every other CT and store its results - the more I increase this number, the lesser keys are guessed. Meaning if I use only 3 Cipher texts
    I get a better result than I do with 11. Which seems a bit strange.
    '''
    for i in range(0,3):
        if i != current_ct_target_num:
            xored_cts[i] = ''
            #xored_cts.append(xor(ct[current_ct_target_num], ct[i]))
            t1= xor(ct[current_ct_target_num], ct[i])
            xored_cts[i] = t1
        else:
            continue
    return xored_cts

def xor(str1,str2):
    t2= []
    for x, y in zip(str1, str2):
        t1= ord(x.zfill(2).decode("hex")) ^ ord(y.zfill(2).decode("hex"))
        t2.append(chr(t1).encode("hex")[1:])

    return ''.join(t2)

def cts_to_ascii(xored_cts):
    #print xored_cts
    t2= []
    #for i in xored_cts:
    for k1, v1 in xored_cts.items():
        t1= ''
        split_str= split_on_specific_char(v1, 2)
        #print split_str
        for j in split_str:
            t1+= chr(int(j,16))
        t2.append(t1)

    return t2

def split_on_specific_char(string,n):
  split_str=[]
  for i in range(0, len(string), n):
    temp1=string[i:i+n]
    split_str.append(temp1)

  return split_str

def analyze(ascii_cts, current_ct_target_num):
    #Try and analyze the cipher text which btw is also m1^m2 at this point
    spaces= []
    keys= []

    for i in range(0,len(ascii_cts),1):
        for count,char in enumerate(ascii_cts[i]):
            o1= ord(char)
            if 97 <= o1 <= 120 or 65 <= o1 <= 90:
                if count not in spaces:
                    spaces.append(count)
                else:
                    keys.append(count)
            else:
                continue

    t1= split_on_specific_char(ct[current_ct_target_num], 2)
    sp1= ord(' ')

    key= {}
    for position in keys:
        t2=ord(t1[position].zfill(2).decode("hex"))
        key[position]= chr(t2^sp1)

    return key

def decrypt(final_keys):
    #Use all the keys found to decrypt the final text
    for i in range(0, len(ct)):
        if i==5 or i==10:
            print '+'*100
            t1= split_on_specific_char(ct[i], 2)
            for count, char in enumerate(t1):
                #c1+=1
                if final_keys.has_key(count):
                    t2=ord(char.zfill(2).decode("hex"))
                    x= t2 ^ ord(final_keys[count])
                    if 97 <= x <=120 or 65 <= x <= 90 or x==32:
                        print chr(x),
                    else:
                        print '_',
                else:
                    print '_',
            print

if __name__ == "__main__":
    #Get all ciphertext
    ct= get_ciphertexts(inputfile)

    #If you know most of the plain text but you are fine tuning, this is what you need to call
    final_keys= {}

    for i in range(0, len(ct)):
        #XOR the 1st ciphertext with all the others
        xored_cts= xor_ciphertexts(ct, i)

       #For each set of XORed texts, convert all the C1^C2 texts to ASCII
        ascii_cts= cts_to_ascii(xored_cts)

       #Analyze
        key= analyze(ascii_cts, i)
        final_keys.update(key)

    #Try and decrypt using the keys obtained
    decrypt(final_keys)
