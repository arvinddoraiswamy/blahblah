import sys
import re

def get_input(filename):
    with open(filename, 'r') as f:
        insts= f.read().splitlines()
    return insts

def handle_rect(pixels, instruction):
    (xlimit,ylimit)= instruction[1].split('x')
    for x in range(0, int(xlimit)):
        for y in range(0, int(ylimit)):
            if (x,y) not in pixels:
                pixels.append((x,y))
            else:
                continue

    return pixels

def handle_column(pixels, instruction):
    colnum= instruction[2].split('=')[1]
    distance= int(instruction[4])
    newpixels= []
    oldpixels= []

    for entry in pixels:
        if int(entry[0]) == int(colnum):
            oldpixels.append(entry)
            t1= (entry[1] + distance ) % ymax
            newpixels.append((entry[0], t1))
        else:
            continue

    for pixel in oldpixels:
        pixels.remove(pixel)

    for pixel in newpixels:
        pixels.append(pixel)

    return pixels

def handle_row(pixels, instruction):
    rownum= instruction[2].split('=')[1]
    distance= int(instruction[4])
    newpixels= []
    oldpixels= []

    for entry in pixels:
        if int(entry[1]) == int(rownum):
            t1= (entry[0] + distance ) % xmax
            oldpixels.append(entry)
            newpixels.append((t1, entry[1]))
        else:
            continue

    for pixel in oldpixels:
        pixels.remove(pixel)

    for pixel in newpixels:
        pixels.append(pixel)

    return pixels

if __name__ == "__main__":
    filename= '8.txt'
    insts= get_input(filename)
    pixels= []
    xmax= 50
    ymax= 6

    for inst in insts:
        t1= inst.split(' ')
        if 'rect' in t1:
            pixels= handle_rect(pixels, t1)
        elif 'row' in t1:
            pixels= handle_row(pixels, t1)
        elif 'column' in t1:
            pixels= handle_column(pixels, t1)

    print 'There are', len(pixels), ' pixels that are lit'

    for y in range(0, ymax):
        row= ''
        for x in range(0, xmax):
            if (x,y) in pixels:
                row += '|'
            else:
                row += ' '

        print row
