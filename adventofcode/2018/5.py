'''
tl;dr Part 1 - Compare adjacent chars, delete them from a duplicated string if they are equal and keep calling the function till not a single pair matches.
tl;dr Part 2 - Reuse Part 1 code. Except you need to go from a-z, substitute the character throughout the string and THEN call the Part 1 function
'''
import re
import operator

def destroy(data):
    i = 0
    match = False
    s1 = list(data)
    while i < len(data)-1:
        if i != len(data):
            if data[i] == data[i+1].swapcase():
                del(s1[i:i+2])
                match = True
                break
            else:
                i += 1

    result = ''.join(s1)
    return result, match

#Part 1
#with open('dump') as f:
with open('5.txt') as f:
    data = f.read().rstrip()

match = True
result= data
while match:
    result, match = destroy(result)

print("Part 1:", len(result))
print('-' * 10)

#Part 2
s1=data
char_length_map = {}
for ch in [chr(x) for x in range(ord('a'), ord('z')+1)]:
    print("Calculating for", ch)
    s1=re.sub(ch, '', s1, flags=re.IGNORECASE)

    match = True
    result= s1
    while match:
        result, match = destroy(result)
    char_length_map[ch] = len(result)
    s1=data

c1=[]
c1 = sorted(char_length_map.items(), key=operator.itemgetter(1))
print("Part 2:", c1[0][1])
