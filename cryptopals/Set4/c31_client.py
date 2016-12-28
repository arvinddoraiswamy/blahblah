import requests
import datetime

url= 'http://localhost:9000/test?'
file_qs='file=teddy&'
sig_qs ='signature='

siglen= 40
guessed_bytes= ''

min_time_diff= 50
byte_count= 0

''' http://localhost:9000/test?file=foo&signature=24b2d4322e50bf57c88697644e2fd1450794ab5c '''
while len(guessed_bytes) < siglen:
    byte_count += 1
    match_detector_time = min_time_diff * byte_count

    for byte in range(0,255):
        req_url= url+file_qs+sig_qs+guessed_bytes
        diff= siglen - len(guessed_bytes)
        req_url += hex(byte)[2:].zfill(2)

        start_time= datetime.datetime.now()
        resp= requests.get(req_url)
        end_time= datetime.datetime.now()
        diff= end_time - start_time
        time_diff= int(diff.total_seconds() * 1000)
        
        if time_diff > match_detector_time:
            print 'Guessed byte', byte_count, hex(byte)[2:]
            guessed_bytes += hex(byte)[2:].zfill(2)
            break
        else:
            continue

req_url= url+file_qs+sig_qs+guessed_bytes
resp= requests.get(req_url)
if resp.content == '500':
    print 'Match not found'
else:
    print 'Match found', guessed_bytes
