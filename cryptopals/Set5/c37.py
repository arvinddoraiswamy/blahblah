import web
import collections
import random
import time
import hashlib
import hmac
import base64
import pickle

#http://localhost:9000/test?userparam=uservalue
#http://webpy.org/docs/0.3/sessions
urls = (
    '/init/?', 'init'
)

web.config.debug= False
app= web.application(urls, locals())
session= web.session.Session(app, web.session.DiskStore('sessions')) 

N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
g= 2
k= 3

class init:
    ''' Get client parameters and send back B so the client can calculate the HMAC and send it back '''
    def getB(self, I, A, P, b, salt):
        xH= hashlib.sha256(str(salt) + str(P)).hexdigest()
        x= int(xH, 16)
        v= pow(g, x, N)
        B= (k * v) + pow(g, b, N)
        return B

    ''' This calculates the correct HMAC for a specific user and password '''
    def calc_correct_hmac(self, I, A, P, b, salt):
        xH= hashlib.sha256(str(salt) + str(P)).hexdigest()
        x= int(xH, 16)
        v= pow(g, x, N)
        B= (k * v) + pow(g, b, N)
        uH= hashlib.sha256(str(A) + str(B)).hexdigest()
        u = int(uH, 16)

        t1= long(A) * pow(v, u, N)
        S= pow(t1, b, N)
        print 'Secret becomes ', S

        sKey= hashlib.sha256(str(S)).hexdigest()
        print 'Key ', sKey

        shmac = hmac.new(sKey, msg=str(salt), digestmod=hashlib.sha256).hexdigest()
        return shmac

    def GET(self):
        user_data= web.input()
        if 'hmac' in user_data.keys():
            with open('tmpsess','r') as f:
                expected_hmac= f.read()

            if user_data.hmac == expected_hmac:
                return 'Login succeeded'
            else:
                return 'Login failed'    
        else:
            session.salt= random.randint(0, pow(2,32))
            session.b= random.getrandbits(256)
            session.A= user_data.A
            session.I= user_data.I

            #Only if the client sends the right password, should this match. Ensure that all other parameters are the same, only the password changes :)
            correctP= 'teddybear'
            session.expected_hmac= self.calc_correct_hmac(session.I, session.A, correctP, session.b, session.salt)

            #Do this so that, the client can calculate the hmac for whatever password he sent
            P= user_data.P
            B= self.getB(session.I, session.A, P, session.b, session.salt)
            with open('tmpsess','w') as f:
                f.write(session.expected_hmac)
            return session.salt, B

if __name__ == "__main__":
    app.run()
