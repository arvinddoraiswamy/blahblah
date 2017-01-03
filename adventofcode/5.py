import hashlib

if __name__ == '__main__':
    '''
    Go through a series of numbers with a prefix attached and hash all of them using MD5. The first 8 hashes that start with five 0s are your target. The 6th char of each of these hashes is 1 char of the final password.
    '''
    input= 'reyedfim'
    count= 0
    hashes= []
    hashes2= []
    while len(hashes) <= 8:
        t1= ''
        t1= input + str(count)
        h1= hashlib.md5(t1).hexdigest()

        if h1[0:5] == '00000':
            print 'Hash 1 found at count', count,'-',h1
            hashes.append(h1[5:6])
        count += 1
    print 'The password is', ''.join(hashes)[0:8]

    count= 0
    t1= ''
    for x in range(0,8):
        hashes2.append('')

    while '' in hashes2:
        t1= ''
        t1= input + str(count)
        h1= hashlib.md5(t1).hexdigest()

        if h1[0:5] == '00000':
            pos= int(h1[5:6], 16)
            char= h1[6:7]
            if 0 <= pos <= 7 and hashes2[pos] == '':
                print 'Hash 2 found at count', count,'-', h1
                hashes2[pos]= char
        count += 1
    print 'The second password is', ''.join(hashes2)[0:8]
