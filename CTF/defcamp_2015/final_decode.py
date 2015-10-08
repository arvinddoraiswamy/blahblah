import sys

inputfile= 'c100'
def get_ciphertexts(inputfile):
    with open(inputfile,'r') as f:
        t1= f.readlines()

    ct= [i.rstrip("\n") for i in t1]
    return ct

def split_on_specific_char(string,n):
  split_str=[]
  for i in range(0, len(string), n):
    temp1=string[i:i+n]
    split_str.append(temp1)

  return split_str

def decrypt(ct):
    p1='a stream cipher generates successive elements of the keystream based on an internal state'
    p2= {}
    c1=ct[5]
    c2= ct[10]
    split_c1= split_on_specific_char(c1,2)    
    split_c2= split_on_specific_char(c2,2)    

    key= {}
    for count,char in enumerate(split_c1):
        key[count]= ord(char.decode("hex")) ^ ord(p1[count])

    for encstring in ct:
        p2= {}
        count= 0
        answer= ''
        split_enc= split_on_specific_char(encstring,2)    
        for count,char in enumerate(split_enc[0:61]):
            p2[count]= ord(char.decode("hex")) ^ key[count]
        for k1,v1 in p2.items():
            answer += chr(v1)
        print answer

if __name__ == "__main__":
    ct= get_ciphertexts(inputfile)
    decrypt(ct)
