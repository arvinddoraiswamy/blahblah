import sys
import os
import web
import collections
import random
import hashlib
import hmac

#Adding directory to the path where Python searches for modules
#cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
#sys.path.insert(0, cmd_folder)
#import block

#http://localhost:9000/test?userparam=uservalue
urls = (
    '/init/?', 'init',
    '/check/?', 'check'
)
class check:
    def GET(self):
        user_data= web.input()
        init.GET()
        print user_data.hmac

class init:
    ''' Get user input '''
    def GET(self):
        #Common parameters for both client and server
        N= 0xe088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
        g= 2
        k= 3
        I= 'teddy@boo.org'
        P= 'teddybear'

        user_data= web.input()
        C_I= user_data.I
        C_A= user_data.A

        S_saved, S_B= self.S_salt_B_gen(g, N, P, k, C_I, C_A)
        S_u         = self.S_uH(C_A, S_B)

        t1= long(C_A) * pow(S_saved.v, S_u, N)
        S= pow(t1, S_saved.b, N)
        sKey= hashlib.sha256(str(S)).hexdigest()

        shmac = hmac.new(sKey, msg=str(S_saved.salt), digestmod=hashlib.sha256).digest()
        return S_saved.salt, S_B, shmac
    
    def S_uH(self, C_A, S_B):
        uH= hashlib.sha256(str(C_A) + str(S_B)).hexdigest()
        u = int(uH, 16)
        return u

    def S_salt_B_gen(self, g, N, P, k, C_I, C_A):
        serverdata= collections.namedtuple('serverdata', 'salt v g N P b')

        salt= random.randint(0, pow(2,32))
        xH= hashlib.sha256(str(salt) + str(P)).hexdigest()
        x= int(xH, 16)
        v= pow(g, x, N)

        b= random.getrandbits(256)
        S_saved= serverdata(salt=salt, v=v, g=g, N=N, P=P, b=b)
        B= (k * S_saved.v) + pow(g, b, N)

        return S_saved, B

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
