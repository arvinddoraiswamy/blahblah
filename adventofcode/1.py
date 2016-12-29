def find_destination(start_dir):
    #Read instructions
    with open('1.txt') as f:
        path= f.read()[:-1]
    t1= path.split(', ')
    
    #Set origin and initialize other stuff
    x=0
    y=0
    startx= x
    starty= y
    path_coords= []
    dup= []

    #Loop over each instruction and move depending on the direction you face
    for inst in t1:
        nob= int(inst[1:])
        #Right turns
        if inst.startswith('R') and start_dir == 'N':
            for i in range(x+1, x+nob+1):
                t2= (i,y)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            x += nob
            start_dir= 'E'
            continue
        if inst.startswith('R') and start_dir == 'S':
            for i in range(x-1, x-nob-1, -1):
                t2= (i,y)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            x -= nob
            start_dir= 'W'
            continue
        if inst.startswith('R') and start_dir == 'E':
            for i in range(y-1, y-nob-1, -1):
                t2= (x,i)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            y -= nob
            start_dir= 'S'
            t2= (x,y)
            path_coords.append(t2)
            continue
        if inst.startswith('R') and start_dir == 'W':
            for i in range(y+1, y+nob+1):
                t2= (x,i)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            y += nob
            start_dir= 'N'
            continue

        #Left turns
        if inst.startswith('L') and start_dir == 'N':
            for i in range(x-1, x-nob-1, -1):
                t2= (i,y)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            x -= nob
            start_dir= 'W'
            continue

        if inst.startswith('L') and start_dir == 'S':
            for i in range(x+1, x+nob+1):
                t2= (i,y)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            x += nob
            start_dir= 'E'
            continue

        if inst.startswith('L') and start_dir == 'E':
            for i in range(y+1, y+nob+1):
                t2= (x,i)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            y += nob
            start_dir= 'N'
            continue

        if inst.startswith('L') and start_dir == 'W':
            for i in range(y-1, y-nob-1, -1):
                t2= (x,i)
                if t2 not in path_coords:
                    path_coords.append(t2)
                else:
                    dup.append(t2)
            y -= nob
            start_dir= 'S'
            continue

    finalx= x - startx
    finaly= y - starty
    distance= abs(finalx) + abs(finaly)
    return distance, dup[0]

if __name__ == '__main__':
    '''
    Set the start direction, and increment X and Y coordinates as you execute each instruction. The add/subtract will differ depending on the direction you are traveling in. Keep a track of every block you pass. The moment you see a duplicate, add that to a separate list.
    '''
    start_dir= 'N'
    distance, dup= find_destination(start_dir)
    print 'Total distance is', distance
    print 'Visited distance is', abs(dup[0]) + abs(dup[1])
