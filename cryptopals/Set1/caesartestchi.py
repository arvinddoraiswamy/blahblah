import operator
import sys
import re

def letter_frequency(string):
  letter_count= {}
  #letter_count[' '] = 0
  letter_count['e'] = 0
  letter_count['t'] = 0
  letter_count['a'] = 0
  letter_count['o'] = 0
  letter_count['i'] = 0
  letter_count['n'] = 0
  letter_count['s'] = 0
  letter_count['h'] = 0
  letter_count['r'] = 0
  letter_count['d'] = 0
  letter_count['l'] = 0
  letter_count['u'] = 0
  letter_count['c'] = 0
  letter_count['m'] = 0
  letter_count['w'] = 0
  letter_count['f'] = 0
  letter_count['y'] = 0
  letter_count['g'] = 0
  letter_count['p'] = 0
  letter_count['b'] = 0
  letter_count['v'] = 0
  letter_count['k'] = 0
  letter_count['x'] = 0
  letter_count['j'] = 0
  letter_count['q'] = 0
  letter_count['z'] = 0

  split_str= list(string)
  for i in range(0,len(split_str)):
    if split_str[i] == 'e':
      letter_count['e']+=1
    elif split_str[i] == 't':
      letter_count['t']+=1
    elif split_str[i] == 'a':
      letter_count['a']+=1
    elif split_str[i] == 'o':
      letter_count['o']+=1
    elif split_str[i] == 'i':
      letter_count['i']+=1
    elif split_str[i] == 'n':
      letter_count['n']+=1
    elif split_str[i] == 's':
      letter_count['s']+=1
    elif split_str[i] == 'h':
      letter_count['h']+=1
    elif split_str[i] == 'r':
      letter_count['r']+=1
    elif split_str[i] == 'd':
      letter_count['d']+=1
    elif split_str[i] == 'l':
      letter_count['l']+=1
    elif split_str[i] == 'u':
      letter_count['u']+=1
    elif split_str[i] == 'c':
      letter_count['c']+=1
    elif split_str[i] == 'm':
      letter_count['m']+=1
    elif split_str[i] == 'w':
      letter_count['w']+=1
    elif split_str[i] == 'f':
      letter_count['f']+=1
    elif split_str[i] == 'y':
      letter_count['y']+=1
    elif split_str[i] == 'g':
      letter_count['g']+=1
    elif split_str[i] == 'p':
      letter_count['p']+=1
    elif split_str[i] == 'b':
      letter_count['b']+=1
    elif split_str[i] == 'v':
      letter_count['v']+=1
    elif split_str[i] == 'k':
      letter_count['k']+=1
    elif split_str[i] == 'x':
      letter_count['x']+=1
    elif split_str[i] == 'j':
      letter_count['j']+=1
    elif split_str[i] == 'q':
      letter_count['q']+=1
    elif split_str[i] == 'z':
      letter_count['z']+=1
    #elif split_str[i] == ' ':
    #  letter_count[' ']+=1

  return letter_count

def normalizeString(string):
  #Convert string to lower case
  string= string.lower()

  #Substitute carriage return with space
  #string= re.sub('[\r]',' ',string)

  #Remove everything other than lower case a-z and space
  #string= re.sub('[^a-z ]','',string)
  string= re.sub('[^a-z]','',string)
  return string

def split_on_specific_char(string,n):
  split_str=[]
  for i in range(0, len(string), n):
    temp1=string[i:i+n]
    split_str.append(temp1)

  return split_str

def rotate_string_entire_alphabet(string):
  #Alphabet hash. z gets 0 because it's mod 26.
  alphabet={'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':0}

  #Split on every character
  split_str=split_on_specific_char(string,1)
  s2= {}

  #Rot 1 to Rot 26
  for j in range(0,26):
    int_rotated_str=[]
    count=0
    #Calculate and store numbers
    for i in split_str:
      if i in alphabet:
        t1=(alphabet[i]+j)%26
        int_rotated_str.append(t1)
        count+=1
      else:
        int_rotated_str.append(i)

    #Get mapped alphabet for the number stored a while ago
    rotated_str=''
    for i in int_rotated_str:
      flag=0
      for key in alphabet.keys():
        if i == alphabet[key]:
          flag=1
          rotated_str=rotated_str+key
      if flag == 0:
        rotated_str=rotated_str+str(i)

    s2[j]=rotated_str

  return s2

def frequencyChiSquare(string):
    expected_count= {}

    '''
    http://www.data-compression.com/english.shtml
    '''
    englishLetterFreq = {'E': 12.702, 'T': 9.056, 'A': 8.167, 'O': 7.507, 'I': 6.966, 'N': 6.749, 'S': 6.327, 'H': 6.094, 'R': 5.987, 'D': 4.253, 'L': 4.025, 'C': 2.782, 'U': 2.758, 'M': 2.406, 'W': 2.361, 'F': 2.228, 'G': 2.015, 'Y': 1.974, 'P': 1.929, 'B': 1.492, 'V': 0.978, 'K': 0.772, 'J': 0.153, 'X': 0.150, 'Q': 0.095, 'Z': 0.074}
    #expected_score= {'a':0.0651738,'b':0.0124248,'c':0.0217339,'d':0.0349835,'e':0.1041442,'f':0.0197881,'g':0.0158610,'h':0.0492888,'i':0.0558094,'j':0.0009033,'k':0.0050529,'l':0.0331490,'m':0.0202124,'n':0.0564513,'o':0.0596302,'p':0.0137645,'q':0.0008606,'r':0.0497563,'s':0.0515760,'t':0.0729357,'u':0.0225134,'v':0.0082903,'w':0.0171272,'x':0.0013692,'y':0.0145984,'z':0.0007836,' ':0.1918182}

    #print len(string)
    string= normalizeString(string)
    #print len(string)

    if len(string) <= 0:
        return -1

    lc= letter_frequency(string)
    expected_count= {key:expected_probability/100 * len(string) for key,expected_probability in englishLetterFreq.items()}

    '''
    print lc.items()
    print
    print expected_count.items()
    print
    print
    '''

    '''
    http://practicalcryptography.com/cryptanalysis/text-characterisation/chi-squared-statistic/
    '''
    total_chi_square= 0
    for letter,no_of_occurences in lc.items():
        #print letter,'-',expected_count[letter]
        chi_square_per_letter= pow(abs(no_of_occurences - expected_count[letter.upper()]), 2)/expected_count[letter.upper()]
        #print letter, chi_square_per_letter
        total_chi_square+= chi_square_per_letter

    return total_chi_square

if __name__ == "__main__":
    chi_scores= {}
    string= 'aoljhlzhyjpwolypzvulvmaollhysplzaruvduhukzptwslzajpwolyzpapzhafwlvmzbizapabapvujpwolypudopjolhjoslaalypuaolwshpualeapzzopmalkhjlyahpuubtilyvmwshjlzkvduaolhswohila'    
    rotated_strings= rotate_string_entire_alphabet(string)

    print string
    for s,v in rotated_strings.items():
        chi_scores[str(s)+':'+v]= frequencyChiSquare(v)

    for s,v in sorted(chi_scores.items(), key= operator.itemgetter(1)):
        print s[0:18],v
