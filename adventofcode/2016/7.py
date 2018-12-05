import sys
import re

def get_input(filename):
    with open(filename, 'r') as f:
        ips= f.read().splitlines()
    return ips

def getTLS():
    final= []
    pattern= '\[(.*?)\]'
    flag= 0

    for ip in ips:
        for offset in range(0, len(ip) - 3):
            t1= ip[offset:offset+4]
            t2= [t1[x:x+2] for x in range(0, len(t1), 2)]
            t3= list(t2[0])
            if t3[0] != t3[1]:
                if t2[0] == t2[1][::-1]:
                    squares= re.findall(pattern, ip)
                    for sq_ip in squares:
                        for sq_offset in range(0, len(sq_ip) - 3):
                            t4= sq_ip[sq_offset:sq_offset+4]
                            t5= [t4[y:y+2] for y in range(0, len(t4), 2)]
                            t6= list(t5[0])
                            if t6[0] != t6[1]:
                                if t5[0] == t5[1][::-1]:
                                    flag= 1
                                    break

                    if flag == 1:
                        flag= 0
                        break
                    else:
                        final.append(ip)
                        break
            else:
                continue

    print 'There are ', len(final), 'IPs that support TLS'

def getSSL():
    pattern= '\[(.*?)\]'
    final= []

    #Get all hypernets inside bracket. Multiple hypernets get detected correctly
    for ip in ips:
        #print 'IP'
        #print ip
        outside= []
        inside= []
        t2= []
        i= 0

        squares= re.findall(pattern, ip)
        for sq_ip in squares:
            for sq_offset in range(0, len(sq_ip) - 2):
                inside.append(sq_ip[sq_offset:sq_offset+3])

        #print 'Inside'
        #print inside
        while i <= len(ip)-3:
            if ip[i] == '[' or '[' in ip[i:i+3] or ']' in ip[i:i+3]:
                i += 1
                while ip[i] != ']':
                    i += 1
                    continue
                i += 1
            else:
                t1= list(ip[i:i+3])
                t2.append(''.join(t1))
                if t1[0] == t1[2] and t1[0] != t1[1]:
                    outside.append(''.join(t1))
                i += 1

        #print 'Outside before filtering'
        #print t2
        #print 'Outside after filtering'
        #if len(outside) > 0:
        #    print outside

        for x in outside:
            t3= list(x)
            t4= t3[1] + t3[0] + t3[1]
            if t4 in inside:
                final.append(ip)
                break
        #print '-' * 10

    print len(final)

if __name__ == "__main__":
    filename= '7.txt'
    ips= get_input(filename)

    #getTLS()
    getSSL()
