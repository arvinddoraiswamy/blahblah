import requests
import datetime
import operator
import sys

url= 'http://localhost:9000/test?'
file_qs='file=fddoo&'
sig_qs ='signature='

siglen= 40
byte_count= 0
guessed_bytes= ''
req_url= ''

''' http://localhost:9000/test?file=foo&signature=24b2d4322e50bf57c88697644e2fd1450794ab5c '''
''' http://localhost:9000/test?file=fddoo&signature=6f62e47b625aeec1cb239258523dd7e03d4cb906 '''
while len(guessed_bytes) < siglen:
    req_time= {}
    byte_count += 1
    for byte in range(0,256):
        req_url= url+file_qs+sig_qs+guessed_bytes
        diff= siglen - len(guessed_bytes)
        req_url += hex(byte)[2:].zfill(2)

        start_time= datetime.datetime.now()
        resp= requests.get(req_url)
        end_time= datetime.datetime.now()
        diff= end_time - start_time
        req_time[hex(byte)]= diff.total_seconds()

    sorted_req_time= []
    for key, value in sorted(req_time.items(), key=operator.itemgetter(1)):
        sorted_req_time.append(key)

    print 'Guessed byte', byte_count, sorted_req_time[-1][2:].zfill(2)
    guessed_bytes += sorted_req_time[-1][2:].zfill(2)

req_url= url+file_qs+sig_qs+guessed_bytes
resp= requests.get(req_url)
if resp.content == '500':
    print 'Match not found'
else:
    print 'Match found', guessed_bytes
