import re
from collections import Counter,OrderedDict,deque

def get_input(filename):
    with open(filename, 'r') as f:
        rooms= f.read().splitlines()
    return rooms

def validateRoom(name, sectorId, checksum):
    status= 0
    name1= re.sub(r'-','',name)
    t1= list(name1)
    count_dict= Counter(t1)

    count= {}
    for k,v in count_dict.items():
        if v not in count.keys():
            count[v]= k
        else:
            count[v] += k

    for k,v in count.items():
        count[k]= ''.join(sorted(v))

    count= OrderedDict(sorted(count.items(), reverse=True))
    expected_checksum= ''
    for k,v in count.items():
        expected_checksum += v

    if checksum == expected_checksum[0:5]:
        status= 1

    return status

def decrypt_room_name(name, sectorId):
    alphabet={'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
    rotate_count= int(sectorId) % 26
    t1= list(name)

    decrypted_room= ''
    for letter in t1:
        if letter in alphabet.keys():
            v= (alphabet[letter] + rotate_count) % 26
            for k1,v1 in alphabet.items():
                if v1 == v:
                    decrypted_room += k1
                    break
        elif letter == '-':
            decrypted_room += ' '
        else:
            continue

    return decrypted_room

if __name__ == '__main__':
    '''
    There's a large number of rooms, some of which are real. Find all of them and add their sector IDs for the answer.
    '''
    filename= '4.txt'
    rooms= get_input(filename)
    pattern= r'(([a-z]*-)*)(\d*)\[(.*)\]'
    regex= re.compile(pattern)
    total= 0

    for room in rooms:
        match= regex.match(room)
        if match:
            #This matches the entire group of 'letters-'. The nested parentheses look ugly but seem to work.
            name= match.group(1)
            sectorId= match.group(3)
            decrypted_room= decrypt_room_name(name[:-1], sectorId)
            checksum= match.group(4)
            status= validateRoom(name, sectorId, checksum)

            if status == 1:
                total += int(sectorId)

            if 'north' in decrypted_room.lower():
                print sectorId, decrypted_room

        else:
            continue

    print total
