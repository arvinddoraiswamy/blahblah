import sys
import os
import web
import time
import datetime
from hashlib import sha1

#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)
import block

#http://localhost:9000/test?file=foo&signature=46b4ec586117154dacd49d664e5d63fdc88efb51
urls = (
    '/test/?', 'test'
)

class test:
    ''' Get user input '''
    def GET(self):
        user_data= web.input()
        #user_hmac= self.hmac(user_data.file)
        #status= self.secure_compare(user_hmac, correct_hmac)

        #This is what the user should send
        correct_hmac= self.hmac('foo')

        #This is what the user actually sent
        user_hmac= str(user_data.signature)
        status= self.insecure_compare(user_hmac, correct_hmac)

        if status == 1:
            return '200'
        elif status == 0:
            return '500'

    ''' Compare in the wrong way which introduces an artificial timing leak'''
    def insecure_compare(self, user_hmac, correct_hmac):
        l1= [user_hmac[count:count+2] for count in range(0, len(user_hmac), 2)]
        l2= [correct_hmac[count:count+2] for count in range(0, len(correct_hmac), 2)]

        status= 1
        for count in range(0, len(l1)):
            if l1[count] == l2[count]:
                time.sleep(50.0/1000.0)
                continue
            else:
                status= 0
                return status

        return status

    ''' Compare in the correct way '''
    def secure_compare(self, user_hmac, correct_hmac):
        if user_hmac == correct_hmac:
            return 1
        else:
            return 0

    ''' Calculate HMAC for any user input '''
    def hmac(self, p1):
        key= 'teddy'
        blocksize= 64
        if len(key) > blocksize:
            key = sha1(key).hexdigest()
        if len(key) < blocksize:
            diff= blocksize - len(key)
            key= key + '\x00' * diff
            o_key_pad = block.xor('\x5c' * blocksize, key)
            i_key_pad = block.xor('\x36' * blocksize, key)

            m1= i_key_pad + p1
            h_m1= sha1(m1).hexdigest()
            m2= o_key_pad + h_m1
            h_m2= sha1(m2).hexdigest()
        return h_m2

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
