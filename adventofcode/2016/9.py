import sys
import re

def get_input(filename):
    with open(filename, 'r') as f:
        markers= f.read().splitlines()
    return ''.join(markers)

def version1(sequence):
    final= ''
    offset= 0
    while offset < len(sequence):
        t1= ''
        if sequence[offset] != '(':
            final += sequence[offset]
            offset += 1
        else:
            offset +=1
            while sequence[offset] != ')':
                t1 += sequence[offset]
                offset += 1
            offset += 1
            t2= t1.split('x')
            t3= sequence[offset:offset+int(t2[0])]
            final += t3 * int(t2[1])
            offset += int(t2[0])

    return final

def version2(sequence):
    offset= 0
    final_len= 0

    #print 'Original sequence', sequence
    while offset < len(sequence):
        t1= ''
        if sequence[offset] != '(':
            final_len += 1
            offset += 1
        else:
            offset +=1
            while sequence[offset] != ')':
                t1 += sequence[offset]
                offset += 1
            offset += 1
            t2= t1.split('x')
            sequence=  sequence[offset:offset+int(t2[0])] * int(t2[1]) + sequence[offset + int(t2[0]):]
            offset= 0
            #print 'split by', t2
            #print 'new sequence', sequence
            #print '-' * 10

    return final_len

if __name__ == "__main__":
    filename= '9.txt'
    sequence= get_input(filename)
    sequence= re.sub(' ','',sequence)
    #final= version1(sequence)
    #print len(final)    
    final_len= version2(sequence)
    print final_len
