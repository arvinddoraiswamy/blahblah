import os
import sys
#Adding directory to the path where Python searches for modules
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)
import mtrand

if __name__ == "__main__":
    mt= []
    mtrand.init_by_array(19650218)
    n= 1

    for i in range(0, n):
        randomnum= mtrand.genrand_int32()
        mt.append(randomnum)
    mtrand.untemper(mt)
