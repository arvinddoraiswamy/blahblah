require '/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/utility'

inputfile='/home/arvind/Documents/Me/My_Projects/challenges/matasano/cryp7_input_file'
base64decodedfile='/home/arvind/Documents/Me/My_Projects/challenges/matasano/cryp7_base64_decoded_file'
plaintextfile='/home/arvind/Documents/Me/My_Projects/challenges/matasano/cryp7_decrypted'

key='YELLOW SUBMARINE'

Utility.base64_decode_file(inputfile,base64decodedfile)
plaintext=Utility.openssl_decrypt_file_ecb(base64decodedfile,key)

f=File.open(plaintextfile,'w')
f.write(plaintext)
f.close
