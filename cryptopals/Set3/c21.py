'''
Implementing the pseudo code on https://en.wikipedia.org/wiki/Mersenne_Twister. DONT look at the Python code below before you implement it yourself.
Of course, that code is all incomplete :/ so had to reimplement http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/MT2002/CODES/mt19937ar.c in Python

Verify your code against the output here:- http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/MT2002/CODES/mt19937ar.out.  Not ideal, the way I solved this, but I 
couldn't see any other way. I'm not smart enough to read a math paper by the smart dudes who wrote it and implement it.
'''

#Adding directory to the path where Python searches for modules
import os
import sys
cmd_folder = os.path.dirname('/home/arvind/Documents/Me/My_Projects/Git/Crypto/modules/')
sys.path.insert(0, cmd_folder)

#Importing common crypto module
import mtrand

if __name__ == "__main__":
    #Some initialization here to start the whole process
    mtrand.init_by_array(19650218)

    #Extract a number/numbers from the stored number array. Pass 'how_many_numbers' you want as a command-line argument.
    for i in range(0,int(sys.argv[1])):
        randomnum= mtrand.genrand_int32()
        print 'Random number',randomnum
        if i%5==4:
            print
