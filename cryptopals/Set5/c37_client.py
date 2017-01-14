import requests
import random
import hashlib
import hmac

if __name__ == '__main__':
    #Common parameters for both client and server
    N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2
    k= 3
    I= 'teddy@boo.org'
    P= 'teddybear'
    req_url= 'http://localhost:9000/init?'

    #Client to server, send EMail address and A just like in Diffie Hellman
    a= random.getrandbits(256)
    A= pow(g, a, N)
    params= 'I=' + str(I) + '&A=' + str(A) + '&P=' + str(P)
    req_url += params

    #Use server response here and compute the shared secret
    resp= requests.get(req_url)
    t3= resp.content.split(', ')

    uH= hashlib.sha256(str(A) + t3[1][:-2]).hexdigest()
    u = int(uH, 16)

    xH= hashlib.sha256(str(t3[0][1:]) + str(P)).hexdigest()
    x= int(xH, 16)

    t1= long(t3[1][:-1]) - (k * pow(g, x, N))
    t2= a + (u * x)
    S= pow(t1, t2, N)

    cKey= hashlib.sha256(str(S)).hexdigest()
    chmac = hmac.new(cKey, msg=str(t3[0][1:]), digestmod=hashlib.sha256).hexdigest()

    req_url= 'http://localhost:9000/init?hmac='
    req_url += chmac
    resp= requests.get(req_url)
    
    print resp.content
