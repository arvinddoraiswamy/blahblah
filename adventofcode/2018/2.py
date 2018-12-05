#Part 1
with open('2.txt') as f:
#with open('dump') as f:
    data = f.read().rstrip().split('\n')

c2 = 0
c3 = 0
for entry in data:
    m2 = False
    m3 = False
    lc = {}
    for char in entry:
        if char in lc.keys():
            lc[char] += 1
        else:
            lc[char] = 1
    
    for k1,v1 in lc.items():
        if v1 == 2 and m2 is False:
            c2 += 1
            m2 = True
        if v1 == 3 and m3 is False:
            c3 += 1
            m3 = True

print("Checksum: ", c2 * c3)

for i in range(0, len(data)):
    done = False
    for j in range(i+1, len(data)):
        count = 0
        index = []
        l1 = list(data[i])
        l2 = list(data[j])
        
        for k in range(0, len(l1)):
            if count > 1:
                break

            if l1[k] != l2[k]:
                count += 1
                index.append(k)
   
        if count == 1:
            done = True
            break

    if done is True:
        del l1[index[0]]
        print("Match:", ''.join(l1))
        break
