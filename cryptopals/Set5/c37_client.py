import requests
import random
import hashlib
import hmac

def login(a, A):
    N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2
    k= 3
    I= 'teddy@boo.org'
    P= 'teddybear'
    req_url= 'http://localhost:9000/init?'

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
    
    print 'Demonstrating normal case'
    print resp.content

def spoofhmac(a, A):
    k= 3
    I= 'teddy@boo.org'
    P= 'teddybear'
    req_url= 'http://localhost:9000/init?'

    params= 'I=' + str(I) + '&A=' + str(A) + '&P=' + str(P)
    req_url += params

    resp= requests.get(req_url)
    t3= resp.content.split(', ')
    return t3[0][1:]

if __name__ == '__main__':

    ''' Normal case '''
    N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
    g= 2
    a= random.getrandbits(256)
    A= pow(g, a, N)
    #login(a, A)
    print '-' * 10

    '''
    Normally, A is set using a random 'a' that is not predictable or guessable by an MITM attacker. Here though the attacker wants to login without a password
    and controls A completely. Meaning, if a value of A causes the HMAC key to be predictable, they could use the predictable key and calculate the HMAC. They 
    could now send the valid HMAC over and login with any password they choose.
    '''

    #Setting A to 0 and trying to guess HMAC. Anything raised to 0 is 0, so key always == 0
    A=0

    salt= spoofhmac(a, A)
    key= hashlib.sha256('0').hexdigest()
    chmac = hmac.new(key, msg=str(salt), digestmod=hashlib.sha256).hexdigest()
    req_url= 'http://localhost:9000/init?hmac='
    req_url += chmac
    resp= requests.get(req_url)
    print 'Making A 0 as a malicious client'
    print resp.content
    print '-' * 10

    #Setting A to N and trying to guess HMAC. N raised to whatever power is always a multiple of N. *That* result mod N is also always 0
    A=N

    salt= spoofhmac(a, A)
    key= hashlib.sha256('0').hexdigest()
    chmac = hmac.new(key, msg=str(salt), digestmod=hashlib.sha256).hexdigest()
    req_url= 'http://localhost:9000/init?hmac='
    req_url += chmac
    resp= requests.get(req_url)
    print 'Making A N as a malicious client'
    print resp.content
    print '-' * 10

    #Setting A to N*2 and trying to guess HMAC. This too becomes 0 when you do the mod N and hence again always guessable
    A=N*2

    salt= spoofhmac(a, A)
    key= hashlib.sha256('0').hexdigest()
    chmac = hmac.new(key, msg=str(salt), digestmod=hashlib.sha256).hexdigest()
    req_url= 'http://localhost:9000/init?hmac='
    req_url += chmac
    resp= requests.get(req_url)
    print 'Making A N*2 as a malicious client'
    print resp.content
