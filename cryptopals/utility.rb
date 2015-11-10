module Utility

require 'base64'
require 'openssl'

  def Utility.base64_decode_file(inputfile,base64decodedfile)
    t1=''
    f=File.open(inputfile,'r')
    f.each{|line|
      t1.concat(line)
    }
    f.close

    f=File.open(base64decodedfile,'w')
    f.write(Base64.decode64(t1))
    f.close
  end

  def Utility.pad_block(buffer, block_size)
    len_buffer= buffer.length
    if block_size > len_buffer
        t1= block_size % len_buffer
    elsif len_buffer > block_size
        t1= len_buffer % block_size
    else
        t1= block_size
    end

    pad_length= block_size - t1
    pad_character= '\x'+pad_length.to_s.rjust(2,'0')
    pad= pad_character * pad_length
    padded_buffer= buffer+pad
    return padded_buffer
  end
  
  def Utility.xor(string1, string2)
    xored_string= ''
    for i in 0..string2.length-1
        t1= ("#{string1[i]}".ord ^ "#{string2[i]}".ord).chr
        xored_string+= t1
    end

    return xored_string
  end

  def Utility.openssl_encrypt_string_aes(string, key)
    aes= OpenSSL::Cipher.new('aes128')
    aes.encrypt
    aes.key= key
    ciphertext= aes.update(string)+aes.final
    return ciphertext
  end

  def Utility.openssl_decrypt_string_aes(string, key)
    aes= OpenSSL::Cipher.new('aes-128-ecb')
    aes.decrypt
    aes.key= key
    plaintext= aes.update(string)+aes.final
    return plaintext
  end

  def Utility.openssl_decrypt_file_ecb(inputfile,key)
    decipher = OpenSSL::Cipher.new('aes-128-ecb')
    decipher.decrypt
    decipher.key= key

    t1=''
    f=File.open(inputfile,'r')
    f.each{|line|
      t1.concat(line)
    }

    plain=decipher.update(t1)+decipher.final
    return plain
  end

  def Utility.openssl_decrypt_string_ecb(string, key)
    decipher= OpenSSL::Cipher.new('aes-128-ecb')
    decipher.decrypt
    decipher.key= key
    plain= decipher.update(string)+decipher.final
    return plain
  end
  
end
