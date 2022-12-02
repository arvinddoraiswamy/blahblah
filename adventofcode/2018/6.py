import collections
import operator

def getDistance(startX, endX, startY, endY):
    # Get difference of every point with every co-ordinate
    dist={}
    for i in range(startX, endX+1):
        for j in range(startY, endY+1):
            for index,coord in coords.items():
                if (i,j) not in dist.keys():
                    dist[(i,j)] = [abs(coord[0]-i) + abs(coord[1]-j)]
                else:
                    dist[(i,j)].append(abs(coord[0]-i) + abs(coord[1]-j))

    # Compare dist with the actual coordinates and find closest
    d2 = {}
    for k,v in dist.items():
        d1 = collections.Counter(v)
        if d1[min(v)] > 1:
            d2[k] = '.'
            #print(k,v, min(v), d1[min(v)])
        else:
            d2[k] = v.index(min(v))
            #print(k,v, min(v))
    #print('-' * 10)
    return d2

#Part 1
t1 = []
t2 = []
coords = {}

# Get coordinates in right format, as well as the range
#with open('dump') as f:
with open('6.txt') as f:
    count = 0
    for row in f:
        l1 = row.rstrip().replace(' ','').split(',')
        t1.append(l1[0])
        t2.append(l1[1])
        coords[count] = (int(l1[0]), int(l1[1]))
        count += 1

startX=0
startY=0
endX=int(max(t1))
endY=int(max(t2))
print("MaxX:", endX, "MaxY", endY)
print('-' * 10)

d2 = getDistance(startX, endX, startY, endY)
print(d2.keys())
sys.exit(0)


#Start with the column immediately to the right of endX. Once you're done calculating compare it with the values you already have for (endX, y)
match = 1
while match == 1:
    newstartX = endX + 1
    newendX = newstartX
    newstartY = 0
    newendY = endY
    t2 = getDistance(newstartX, newendX, newstartY, newendY) 
    newrc = False
    for y in range(0, endY+1):
        if d2[(endX, y)] == t2[(newstartX, y)]:
            #print("Match: ", (endX, y), d2[(endX,y)], t2[(newstartX, y)])
            match = 0
        else:
            #print("No match:", d2[(endX,y)], t2[(newstartX, y)])
            #endX = newendX
            match = 1
            newrc = True

        #Update dictionary by adding new column
        d2[(newstartX, y)] = t2[(newstartX, y)]

    if newrc:
        endX = newendX


#Next go to the left most column where x becomes -ve. Once you're done here, compare it with what you have for (startX, y)
match = 1
while match == 1:
    newstartX = startX - 1
    newendX = newstartX
    newstartY = 0
    newendY = endY
    t2 = getDistance(newstartX, newendX, newstartY, newendY) 
    newrc = False
    for y in range(0, endY+1):
        if d2[(startX, y)] == t2[(newstartX, y)]:
            #print("Match: ", d2[(startX,y)], t2[(newstartX, y)])
            match = 0
        else:
            #endX = newendX
            match = 1
            newrc = True

        #Update dictionary by adding new column
        d2[(newstartX, y)] = t2[(newstartX, y)]

    if newrc:
        endX = newendX

#Now go to the bottom most row where y becomes +ve. Once you're done here, compare it with what you have for (x, endY)
match = 1
while match == 1:
    newstartX = 0
    newendX = endX
    newstartY = endY + 1
    newendY = newstartY
    t2 = getDistance(newstartX, newendX, newstartY, newendY) 
    newrc = False
    for x in range(0, endX+1):
        if d2[(x, endY)] == t2[(x, newendY)]:
            #print("Match: ", d2[(endX,y)], t2[(newstartX, y)])
            match = 0
        else:
            #endY = newendY
            match = 1
            newrc = True

        #Update dictionary by adding new column
        d2[(x, newstartY)] = t2[(x, newstartY)]

    if newrc:
        endY = newendY

#Now go to the top most row where y becomes -ve. Once you're done here, compare it with what you have for (x, startY)
match = 1
while match == 1:
    newstartX = 0
    newendX = endX
    newstartY = startY - 1
    newendY = newstartY
    newrc = False
    t2 = getDistance(newstartX, newendX, newstartY, newendY) 
    for x in range(0, endX+1):
        if d2[(x, startY)] == t2[(x, newstartY)]:
            #print("Match: ", d2[(endX,y)], t2[(newstartX, y)])
            match = 0
        else:
            match = 1
            newrc = True

        #Update dictionary by adding new column
        d2[(x, newstartY)] = t2[(x, newstartY)]

    if newrc:
        endY = newendY

# Track infinites by looking at the border coordinates
final = {}
infinite = []
for k,v in d2.items():
    print(k,v)
    if v != '.':
        if k[0] == 0 or k[0] == endX or k[1] == 0 or k[1] == endY:
            if v not in infinite:
                infinite.append(v)

        if v not in final.keys():
            final[v] = 1
        else:
            final[v] += 1

#print('-' * 10)
#print("Infinite", infinite)
#print('-' * 10)
#for k,v in final.items():
#    print(k, v)
#print('-' * 10)
count= sorted(final.items(), reverse=True, key=operator.itemgetter(1))
for entry in count:
    #print(entry)
    if entry[0] not in infinite:
        print(entry[1])
        break
    else:
        continue
