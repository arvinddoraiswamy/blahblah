import binascii
import block

key=   '0x71e6efcfb44e362b6e14f7abbecf5503' 
key_in_binary= binascii.a2b_hex(key[2:])
iv=   '0x81d6e5cfb54e352b6e14f8ab9ec45563' 
iv_in_binary=  binascii.a2b_hex(iv[2:])
block_size= 16

def process_and_decrypt_string(encrypted):
    decrypted= block.openssl_cbc_decrypt(encrypted, key_in_binary, iv_in_binary)
    return decrypted

def process_and_encrypt_string(userdata):
    encrypted= block.openssl_cbc_encrypt(userdata, block_size, key_in_binary, iv_in_binary)
    return encrypted

if __name__ == "__main__":
    ''' User 1 sends 3 blocks of plaintext to get encrypted with a set IV and a set key '''
    print 'User 1 sends data'
    userdata1= 'A'*16 + 'B'*16 + 'C'*12
    print 'Encrypting', userdata1
    encrypted1= process_and_encrypt_string(userdata1)
    t1= [encrypted1[x:x+16] for x in range(0, len(encrypted1), 16)]
    for count,bl in enumerate(t1):
        print 'Block', count, repr(bl)
    decrypted1= process_and_decrypt_string(encrypted1)
    print 'Decrypted data', decrypted1
    print '-' * 10

    ''' 
    User 2 sends a DIFFERENT middle block thus changing the encrypted content of the 2nd block and everything after it despite the IV and the key being the same
    '''
    print 'User 2 sends data'
    userdata2= 'A'*16 + 'X'*16 + 'C'*12
    encrypted2= process_and_encrypt_string(userdata2)
    print 'Encrypting', userdata2
    t2= [encrypted2[x:x+16] for x in range(0, len(encrypted2), 16)]
    for count,bl in enumerate(t2):
        print 'Block', count, repr(bl)
    decrypted2= process_and_decrypt_string(encrypted2)
    print 'Decrypted data', decrypted2
