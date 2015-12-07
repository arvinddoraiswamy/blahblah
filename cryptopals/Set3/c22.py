'''
http://security.stackexchange.com/questions/6740/flaw-in-encryption-through-pseudorandom-number-stream-from-pgp-documentation
'''
import os
import sys
import random
import time
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)
import mtrand

if __name__ == "__main__":
    t1= random.randint(40,1000)
    print "Sleeping for ",t1," seconds"
    time.sleep(t1)

    seed= int(time.time())
    print "Seed:", seed
    mtrand.init_by_array(seed)

    t2= random.randint(40,1000)
    print "Sleeping for ",t2," seconds"
    time.sleep(t2)

    num= mtrand.genrand_int32()
    print "First random number is:", num
    print "Lets now try and predict the seed, using the random number. This is just reversing the process."

    print "Getting current timestamp and finding range"
    cur_timestamp= int(time.time())
    for guess in xrange(cur_timestamp-1024,cur_timestamp):
        mtrand.clear_state()
        mtrand.init_by_array(guess)
        g1= mtrand.genrand_int32()
        if g1==num:
            print '-'*75
            print "Seed found in the reverse process. The seed is", guess
            print '-'*75
            break
        else:
            continue
