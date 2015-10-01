import sys
import os
import re
import binascii
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import block

def process_and_decrypt_string(encrypted_tampered):
    admin_string= ';admin=true;'
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])
    iv= '0x29b28d9f2f56c07a8df1778d7408ba79'
    iv_in_binary=  binascii.a2b_hex(iv[2:])

    decrypted_tampered= block.openssl_cbc_decrypt(encrypted_tampered, key_in_binary, iv)
    m1= re.search(admin_string, decrypted_tampered)
    if m1:
        return decrypted_tampered, True
    else:
        return decrypted_tampered, False

def process_and_encrypt_string(prepended_text, userdata, appended_text):
    block_size= 16
    key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
    key_in_binary= binascii.a2b_hex(key[2:])
    iv= '0x29b28d9f2f56c07a8df1778d7408ba79'
    iv_in_binary=  binascii.a2b_hex(iv[2:])

    chars_to_filter= [';','=']
    userdata= block.eat_chars(userdata, chars_to_filter)

    final_str= prepended_text+userdata+appended_text
    padded_final_str= block.pad_block(final_str,block_size) 

    encrypted= block.openssl_cbc_encrypt(padded_final_str, block_size, key_in_binary, iv)

    #Try destroying specific bytes here. Since ; and = are both swallowed up you need to corrupt 2 corresponding bytes in the previous block.
    encrypted_tampered = {}

    '''
    #This bit is useful don't delete it. Uncomment it when you still haven't found out which exact character you need for your solution.
    for i in range(0,256):
        encrypted_tampered[i]= encrypted[0:32]+chr(i)+encrypted[33:38]+chr(i)+encrypted[39:]
    '''
    encrypted_tampered= encrypted[0:32]+chr(117)+encrypted[33:38]+chr(116)+encrypted[39:]
    return encrypted_tampered

if __name__ == "__main__":
    userdata= 'testy stringteddX;adminXtrue'
    prepended_text= 'comment1=cooking%20MCs;userdata='
    appended_text = ';comment2=%20like%20a%20pound%20of%20bacon'

    encrypted_tampered= process_and_encrypt_string(prepended_text, userdata, appended_text)

    decrypted_tampered,is_admin_string_present= process_and_decrypt_string(encrypted_tampered)
    t1= []
    for j in range(0,len(decrypted_tampered)):
        t1.append(decrypted_tampered[j])
        if len(t1) % 16 == 0:
            print ''.join(t1)
            t1= []
        else:
            continue

    '''
    #This bit is useful don't delete it. Uncomment it when you still haven't found out which exact character you need for your solution.

    t1= []
    for i in range(0,256):
        decrypted_tampered, is_admin_string_present= process_and_decrypt_string(encrypted_tampered[i])
        if decrypted_tampered[48] == ';':
            print "Key for ; is:","\t",i
            print '-'*100
            for j in range(0,len(decrypted_tampered)):
                t1.append(decrypted_tampered[j])
                if len(t1) % 16 == 0:
                    print ''.join(t1)
                    t1= []
                else:
                    continue
            break

    for i in range(0,256):
        decrypted_tampered, is_admin_string_present= process_and_decrypt_string(encrypted_tampered[i])
        if decrypted_tampered[54] == '=':
            print "Key for ; is:","\t",i
            print '-'*100
            for j in range(0,len(decrypted_tampered)):
                t1.append(decrypted_tampered[j])
                if len(t1) % 16 == 0:
                    print ''.join(t1)
                    t1= []
                else:
                    continue
            break
    '''
