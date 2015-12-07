(w, n, m, r) = (32, 624, 397, 31)
a= 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18
upper_mask= 0x80000000
lower_mask= 0x7fffffff
mti= n+1
mt= []

def clear_state():
    global mt
    global mti
    mti= n+1
    mt= []

def init_genrand(seed):
    index= n
    mt.append(seed & 0xffffffff)
    for mti in range(1,n):
        t1= 1812433253 * (mt[mti-1] ^ (mt[mti-1] >> 30)) + mti; 
        t1= t1 & 0xFFFFFFFF
        mt.append(t1)
    return mt

def init_by_array(seed):
    init=[0x123, 0x234, 0x345, 0x456]
    length=4

    #This is the seed that's used. If someone knows the seed, attempts at secrecy are basically useless, as they can then predict every random number.
    init_genrand(seed)

    i= 1
    j= 0
    if n>length:
        k= n
    else:
        k= length

    for r1 in range(k,0,-1):
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1664525)) + init[j] + j;
        mt[i] &= 0xffffffff
        i+=1
        j+=1
        if i>=n:
            mt[0] = mt[n-1]
            i=1
        if j>=length:
            j=0

    for r1 in range(n-1,0,-1):
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1566083941)) - i
        mt[i] &= 0xffffffff
        i+=1
        if i>=n:
            mt[0] = mt[n-1] 
            i=1

    mt[0] = 0x80000000

def genrand_int32():
    global mt
    global mti
    y= 0
    if mti >=n:
        if mti == n+1:
            init_genrand(5489)

        kk= 0
        mag01= [0x0, 0x9908b0df]

        for kk in range(0, n-m):
            y = (mt[kk]&upper_mask)|(mt[kk+1]&lower_mask)
            mt[kk] = mt[kk+m] ^ (y >> 1) ^ mag01[y & 0x1]

        for kk in range(kk,n-1):
            y = (mt[kk]&upper_mask)|(mt[kk+1]&lower_mask)
            mt[kk] = mt[kk+(m-n)] ^ (y >> 1) ^ mag01[y & 0x1]


        y = (mt[n-1]&upper_mask)|(mt[0]&lower_mask)
        mt[n-1] = mt[m-1] ^ (y >> 1) ^ mag01[y & 0x1]

        mti = 0

    y= mt[mti]
    mti += 1
    print 'Original number',y
    y= y ^ ((y >> u) & d)
    print 'y1',y
    y= y ^ ((y << s) & b)
    print 'y2',y
    y= y ^ ((y << t) & c)
    print 'y3',y
    y= y ^ (y >> l)
    print '-'*10

    return y

def untemper(mt):
    for num in mt:
        print "Tempered num",num
    print "Now untempering numbers, so I can predict things"
    for num in mt:
        t1= num>>l
        num= num^t1
