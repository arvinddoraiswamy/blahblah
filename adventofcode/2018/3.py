'''
tl;dr - Get all valid co-ordinates for each entry and compare them
'''
import re

#Part 1
with open('3.txt') as f:
#with open('dump') as f:
    data = f.read().replace(' ','').rstrip().split('\n')

final = []
claim_map = {}

for count, entry in enumerate(data):
    t1 = entry.split('@')
    claim_id = t1[0][1:]

    # Extract coordinates
    entry = re.sub('(.*)@', '', entry)
    l1 = entry.split(',')
    left = int(l1[0])
    l1 = l1[1].split(':')
    top = int(l1[0])
    width, height = l1[1].split('x')
    width = int(width)
    height = int(height)
    maxwidth = left + width
    maxheight = top + height

    # Store data per entry
    left1 = left
    while top < maxheight:
        for x in range(left, maxwidth):
            final.append((x, top))
            if claim_id not in claim_map:
                claim_map[claim_id] = [(x, top)]
            else:
                claim_map[claim_id].append((x, top))
        top += 1
        left = left1

counter = {}
for entry in final:
    if entry not in counter.keys():
        counter[entry] = 1
    else:
        counter[entry] += 1

num_dup_claims = 0
unique = {}
for k,v in counter.items():
    if v >= 2:
        num_dup_claims += 1
    elif v == 1:
        unique[k] = 9999

print("Part 1:", num_dup_claims)

for key,value in claim_map.items():
    match = 1
    for v1 in value:
        if v1 not in unique.keys():
            match = 0
            break

    if match == 1:
        print("Part 2:", key)
        break
