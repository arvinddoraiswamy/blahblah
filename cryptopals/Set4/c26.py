import sys
import os
import re
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block

def ctr_process_and_decrypt_string(encrypted_tampered):
    admin_string= ';admin=true;'
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])
    nonce= '\x00' * 8
    decrypted_tampered= block.ctr_decrypt_string(encrypted_tampered, key_in_binary, nonce)
    m1= re.search(admin_string, decrypted_tampered)
    if m1:
        return decrypted_tampered, True
    else:
        return decrypted_tampered, False

    '''
    #Don't delete this bit - its what does the brute force over the whole counterspace
    flag= 0
    for key,value in encrypted_tampered.items():
        decrypted_tampered= block.ctr_decrypt_string(value, key_in_binary, nonce)
        m1= re.search(admin_string, decrypted_tampered)
        if m1:
            flag= 1
            #print key
            return decrypted_tampered, True
        else:
            continue

    if flag == 0:
        return 'Admin string not found - ', False
    '''

def ctr_process_and_encrypt_string(prepended_text, userdata, appended_text):
    block_size= 16
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])
    nonce= '\x00' * 8

    chars_to_filter= [';','=']
    userdata= block.eat_chars(userdata, chars_to_filter)

    final_str= prepended_text+userdata+appended_text
    padded_final_str= block.pad_block(final_str,block_size) 

    encrypted= block.ctr_encrypt_string(padded_final_str, key_in_binary, nonce)

    #Try destroying specific bytes here. Since ; and = are both swallowed up you need to corrupt 2 corresponding bytes in the previous block.
    encrypted_tampered= {}
    '''
    #This bit is useful, don't delete it. Uncomment it when you still haven't found out which exact character you need for your solution.
    for i in range(0,256):
        for j in range(0,256):
            encrypted_tampered[str(i)+'_'+str(j)]= encrypted[0:34]+chr(i)+encrypted[35:40]+chr(j)+encrypted[41:]
    return encrypted_tampered
    '''

    encrypted_tampered= encrypted[0:34]+chr(11)+encrypted[35:40]+chr(24)+encrypted[41:]
    return encrypted_tampered

if __name__ == "__main__":
    userdata= 'TEXadminXtrue'
    prepended_text= 'comment1=cooking%20MCs;userdata='
    appended_text = ';comment2=%20like%20a%20pound%20of%20bacon'

    encrypted_tampered= ctr_process_and_encrypt_string(prepended_text, userdata, appended_text)

    decrypted_tampered,is_admin_string_present= ctr_process_and_decrypt_string(encrypted_tampered)

    t1= []
    for j in range(0,len(decrypted_tampered)):
        t1.append(decrypted_tampered[j])
        if len(t1) % 16 == 0:
            print ''.join(t1)
            t1= []
        else:
            continue

    print 'Admin string present', is_admin_string_present
