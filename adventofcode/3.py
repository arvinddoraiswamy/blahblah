def get_input(filename):
    with open(filename, 'r') as f:
        triangles= f.read().splitlines()
    return triangles

def get_valid_triangles(triangles):
    valid_triangle_count= 0
    for triangle in triangles:
        s1,s2,s3= triangle.split(',')

        if int(s1) + int(s2) <= int(s3):
            continue
        elif int(s2) + int(s3) <= int(s1):
            continue
        elif int(s1) + int(s3) <= int(s2):
            continue

        valid_triangle_count += 1

    print 'There are', valid_triangle_count, 'valid triangles'

if __name__ == '__main__':
    '''
    Each line has the lengths of the sides of a triangle. The sum of any 2 sides must be greater than the 3rd side for the triangle to be valid.
    '''
    filename= '3.txt'
    triangles= get_input(filename)
    #Part 1
    get_valid_triangles(triangles)

    #Part 2
    col1=''
    col2=''
    col3=''
    for triangle in triangles:
        t1=triangle.split(',')
        col1 += t1[0]
        col1 += ','
        col2 += t1[1]
        col2 += ','
        col3 += t1[2]
        col3 += ','

    col1= col1[:-1]
    col2= col2[:-1]
    col3= col3[:-1]

    sides = col1.split(",")
    col1= [",".join(sides[i:i+3]) for i in range(0, len(sides), 3)]

    sides = col2.split(",")
    col2= [",".join(sides[i:i+3]) for i in range(0, len(sides), 3)]

    sides = col3.split(",")
    col3= [",".join(sides[i:i+3]) for i in range(0, len(sides), 3)]

    new_triangles= col1 + col2 + col3
    get_valid_triangles(new_triangles)
