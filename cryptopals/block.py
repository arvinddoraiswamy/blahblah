from Crypto.Cipher import AES
import os
import random
import binascii
import sys
import base64
import re
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)
import utility

def ctr_counter_fixed_nonce_encrypt(string, key, nonce, counter):
    t1= nonce+str(counter).zfill(8)
    t2= openssl_ecb_encrypt(t1, key)
    return t2

def ctr_encrypt(decoded_str, key, nonce):
    blocklen= 16
    list_encrypted= []
    for string in decoded_str: 
        t3= []
        keystream= ''
        counter= len(string)/blocklen + 1
        for i in range(0, counter, 1):
            t3.append(ctr_counter_fixed_nonce_encrypt(string, key, nonce, i))
        keystream= ''.join(t3)
        encrypted= xor(string, keystream)
        list_encrypted.append(encrypted)

    return list_encrypted

def check_pad(blocklen, decrypted):
    l1= len(decrypted)
    last_block= decrypted[l1-16:l1]
    pad_char= last_block[-1]

    valid_pads= []
    for num in range(1,17):
        valid_pads.append(num)

    if ord(pad_char) in valid_pads:
        t1= blocklen-ord(pad_char)
        for char in last_block[t1::]:
            if char == pad_char:
                continue
            else:
                return False
        return True
    else:
        return False

def convert_to_json(email):
    chars_to_filter=['&','=']
    email= eat_chars(email, chars_to_filter)
    query_string= 'email='+email+'&uid=10&role=user'

    #Convert to unicode so you can use isnumeric()
    profile= query_string.decode('utf-8')
    t1= profile.split('&')
    t3= []
    for i in t1:
        t2= i.split('=')
        if not t2[1].isnumeric():
            t2[1]= "\'"+t2[1]+"\'"
        i='='.join(t2)
        t3.append(i)
    profile='&'.join(t3)
    profile= re.sub('=',': ',profile)
    profile= re.sub('&',',\n ',profile)
    profile= '{\n '+profile+'\n}'
    return profile
    

def eat_chars(string,chars_to_filter):
    for char in chars_to_filter:
        string= re.sub(char,'',string)
    return string

def generate_random_string(string_length):
    random_key = os.urandom(string_length)
    return random_key

def break_ecb_random_prepend(plaintext):
    block_size= 16
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])

    #Generate a randomly long (well kinda ;)) string to prepend :). Note that if you change this, the offsets in c14.py will have to be adjusted as well
    rlen= 13
    rstr_prepend= generate_random_string(rlen)

    #This is the target we want to decrypt
    unknown_string= 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    plaintext= rstr_prepend+plaintext+base64.b64decode(unknown_string)
    padded_plaintext= pad_block(plaintext, block_size)
    count= 1

#   #Encrypt string
    encrypted= openssl_ecb_encrypt(padded_plaintext, key_in_binary)
    return encrypted

def break_ecb(plaintext):
    #Generate a random 16 byte long key
    block_size= 16
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])
    unknown_string= 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'

    plaintext= plaintext+base64.b64decode(unknown_string)
    padded_plaintext= pad_block(plaintext, block_size)
    count= 1

    #Detect block size
    while (count <= 16):
        try:
            encrypted= openssl_ecb_encrypt(padded_plaintext[0:count], key_in_binary)
            #print "Block size is ", count
            count= 0
            break
        except ValueError:
            count += 1
            pass

    #Encrypt string and detect ECB from the encrypted contents
    encrypted= openssl_ecb_encrypt(padded_plaintext, key_in_binary)
    are_strings_hex= 1
    t1= utility.get_ecb_blocks(binascii.b2a_hex(encrypted), block_size, are_strings_hex)[:-1]
    blocks= t1.split('_')
    is_aes_mode_ecb= utility.detect_ecb(blocks)
    if is_aes_mode_ecb == 1:
        #print "String is AES encrypted with ECB mode"
        #print '-' * 90
        pass

    return encrypted

def encryption_oracle(plaintext):
    #Generate a random 16 byte long key
    block_size= 16
    keylen= 16
    key=    generate_random_string(keylen)

    #Generate a number between 5 and 10 both inclusive to prepend and append that many bytes to the plaintext. Pad the block.
    random_byte_count= random.randrange(5,11,1)
    random_prefix_suffix_bytes= generate_random_string(random_byte_count)
    plaintext= random_prefix_suffix_bytes+plaintext+random_prefix_suffix_bytes
    padded_plaintext= pad_block(plaintext, block_size)

    #Encrypt with ECB or CBC.
    ecb_or_cbc       = random.randrange(0,2,1)
    if ecb_or_cbc == 0:
        encrypted= openssl_ecb_encrypt(padded_plaintext, key)
    elif ecb_or_cbc == 1:
        random_iv= os.urandom(16)
        encrypted= openssl_cbc_encrypt(padded_plaintext, block_size, key, random_iv)

    are_strings_hex= 1
    t1= utility.get_ecb_blocks(binascii.b2a_hex(encrypted), block_size, are_strings_hex)[:-1]
    blocks= t1.split('_')
    is_aes_mode_ecb= utility.detect_ecb(blocks)

    return is_aes_mode_ecb

def pad_block(buffer, block_size):
    len_buffer= len(buffer)
    if block_size > len_buffer:
        t1= block_size % len_buffer
        pad_length= t1
    elif len_buffer > block_size:
        t1= len_buffer % block_size
        pad_length= block_size - t1
    else:
        pad_length= block_size

    pad_character= (r'\x'+str(pad_length).zfill(2)).decode('string-escape')
    pad= pad_character * pad_length
    padded_buffer= buffer+pad
    return padded_buffer

def xor(string1, string2):
    s2= ''
    for count,t1 in enumerate(string1):
        s2+= chr(ord(string1[count]) ^ ord(string2[count]))

    return s2

def openssl_ecb_encrypt(plaintext, key):
    mode= AES.MODE_ECB
    aes=  AES.new(key, mode)
    ciphertext= aes.encrypt(plaintext)
    return ciphertext

def openssl_ecb_decrypt(ciphertext, key):
    mode= AES.MODE_ECB
    aes=  AES.new(key, mode)
    plaintext= aes.decrypt(ciphertext)
    return plaintext

def openssl_cbc_encrypt(plaintext, block_size, key, iv):
    #Pad plaintext before encrypting it
    padded_plaintext= pad_block(plaintext, block_size)

    #XOR first plaintext block with IV
    xor_with_iv_plaintext= xor(padded_plaintext[0:16], iv)

    #Encrypt first block
    ct= []
    ct0= openssl_ecb_encrypt(xor_with_iv_plaintext, key)
    ct.append(ct0)

    #Encrypt remaining blocks
    for offset in range(16, len(padded_plaintext), 16):
        #XOR next plaintext block with previous ciphertext block
        t3= xor(ct0, padded_plaintext[offset:offset+16])

        #Encrypt the result of the XOR and save it as the ciphertext of the next block. Use this as input for the next block
        ct0= openssl_ecb_encrypt(t3, key)
        ct.append(ct0)

    #Join the ciphertext and return a string
    encrypted= ''.join(ct)
    return encrypted

def openssl_cbc_decrypt(ciphertext, key, iv):
    final_xor_plaintext= []    
    #Decrypt the first block using and XOR with the IV
    decrypted_ciphertext= openssl_ecb_decrypt(ciphertext[0:16], key)
    final_xor_plaintext.append(xor(decrypted_ciphertext, iv))

    #Decrypt all the remaining blocks and XOR with previous ciphertext to get the plaintext for that block
    for offset in range(16, len(ciphertext), 16):
        ctext_per_block= openssl_ecb_decrypt(ciphertext[offset:offset+16], key)
        final_xor_plaintext.append(xor(ctext_per_block, ciphertext[offset-16:offset]))

    #Join the plaintext and return a string
    decrypted= ''.join(final_xor_plaintext)
    return decrypted
